"""CLI que simula partidos con distintas diferencias de atributos totales y
muestra una tabla resumen de victorias, empates, derrotas, % de victoria y
goles medios por bando.
"""

from __future__ import annotations

import argparse
import os
import random

from .ai import AutomaticPlayerAI
from .engine import RulesEngine
from .game_state import MatchResult, Team


def _simulate(
    engine: RulesEngine,
    player: Team,
    opponent: Team,
    seeds: list[int],
) -> tuple[int, int, int, int, int, int, int, int]:
    """Ejecuta un partido por cada semilla recibida y devuelve las estadísticas."""

    wins = draws = losses = 0
    total_goals = 0
    total_bot_goals = 0
    total_cr_draws = 0
    total_bot_red_cards = 0
    total_player_red_cards = 0

    for seed in seeds:
        state = engine.create_match_state(
            player,
            opponent,
            random.Random(seed),
        )
        result: MatchResult = engine.play_match(
            state,
            AutomaticPlayerAI(engine),
        )

        bot_goals = result.bot_goals
        total_goals += result.player_goals
        total_bot_goals += bot_goals
        total_cr_draws += result.cr_draws
        total_bot_red_cards += result.red_cards
        total_player_red_cards += result.player_red_cards

        if result.player_goals > bot_goals:
            wins += 1
        elif bot_goals > result.player_goals:
            losses += 1
        else:
            draws += 1

    return (
        wins,
        draws,
        losses,
        total_goals,
        total_bot_goals,
        total_cr_draws,
        total_bot_red_cards,
        total_player_red_cards,
    )


def _generate_unique_seeds(rng: random.Random, count: int) -> list[int]:
    """Genera exactamente ``count`` semillas únicas de 63 bits.

    No usa random.sample(range(2**63), ...), porque en Windows ese range
    no puede convertirse en un tamaño C ssize_t para ``random.sample``.
    """

    seeds: list[int] = []
    used: set[int] = set()

    while len(seeds) < count:
        seed = rng.getrandbits(63)
        if seed not in used:
            used.add(seed)
            seeds.append(seed)

    return seeds


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Tabla de equilibrio: V/E/D, % de victoria y goles medios "
            "según la diferencia de atributos."
        )
    )
    parser.add_argument(
        "--matches",
        type=int,
        default=100,
        help="Partidos a simular por cada nivel de atributos.",
    )
    parser.add_argument(
        "--bot",
        type=int,
        nargs=3,
        metavar=("DEF", "MED", "AT"),
        default=(15, 15, 15),
        help="Atributos fijos del bot.",
    )
    parser.add_argument(
        "--player-levels",
        type=int,
        nargs="+",
        default=[12, 13, 14, 15, 16, 17, 18],
        help="Valores uniformes (DEF=MED=AT) del equipo del jugador a simular.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Semilla base reproducible. Si se omite, se usa una semilla aleatoria.",
    )
    args = parser.parse_args()

    if args.matches < 1:
        parser.error("--matches debe ser al menos 1.")

    if args.seed is None:
        args.seed = int.from_bytes(os.urandom(8), "big")

    engine = RulesEngine()
    opponent = Team(*args.bot)
    opponent_total = opponent.defense + opponent.midfield + opponent.attack

    # Una única secuencia de semillas para TODA la ejecución.
    # Ejemplo: 100 partidos x 7 niveles = 700 semillas únicas.
    total_matches = args.matches * len(args.player_levels)
    seed_rng = random.Random(args.seed)
    all_seeds = _generate_unique_seeds(seed_rng, total_matches)
    seed_cursor = 0

    print("=" * 88)
    print("      BG FÚTBOL — Informe de equilibrio por diferencia de atributos")
    print("=" * 88)
    print(
        f"Bot fijo: {opponent.defense}/{opponent.midfield}/{opponent.attack}"
        f"  ·  Partidos por nivel: {args.matches}  ·  Semilla base: {args.seed}"
    )
    print(f"Semillas de partido: {total_matches} únicas en toda la ejecución")
    print()

    columns = (
        "Tu equipo",
        "Diferencia (suma)",
        "Victorias",
        "Empates",
        "Derrotas",
        "% Victoria",
        "Goles jugador",
        "Goles bot",
        "CR robadas",
        "Rojas bot",
        "Rojas propias",
    )
    widths = (12, 20, 11, 9, 10, 12, 15, 10, 12, 11, 15)
    print("".join(name.ljust(width) for name, width in zip(columns, widths)))
    print("-" * sum(widths))

    for level in args.player_levels:
        player = Team(level, level, level)
        player_total = level * 3
        gap = opponent_total - player_total

        if gap > 0:
            gap_label = f"+{gap} (peor)"
        elif gap < 0:
            gap_label = f"{gap} (mejor)"
        else:
            gap_label = "0 (igual)"

        level_seeds = all_seeds[seed_cursor:seed_cursor + args.matches]
        seed_cursor += args.matches

        (
            wins,
            draws,
            losses,
            total_goals,
            total_bot_goals,
            total_cr_draws,
            total_bot_red_cards,
            total_player_red_cards,
        ) = _simulate(
            engine,
            player,
            opponent,
            level_seeds,
        )

        win_pct = wins / args.matches * 100
        avg_goals = total_goals / args.matches
        avg_bot_goals = total_bot_goals / args.matches
        avg_cr_draws = total_cr_draws / args.matches
        avg_bot_red_cards = total_bot_red_cards / args.matches
        avg_player_red_cards = total_player_red_cards / args.matches

        row = (
            f"{level}/{level}/{level}",
            gap_label,
            str(wins),
            str(draws),
            str(losses),
            f"{win_pct:.1f}%",
            f"{avg_goals:.2f}",
            f"{avg_bot_goals:.2f}",
            f"{avg_cr_draws:.2f}",
            f"{avg_bot_red_cards:.2f}",
            f"{avg_player_red_cards:.2f}",
        )
        print("".join(value.ljust(width) for value, width in zip(row, widths)))

    print("=" * 88)


if __name__ == "__main__":
    main()
