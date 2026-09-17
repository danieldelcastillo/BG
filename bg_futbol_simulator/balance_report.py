"""CLI que simula partidos con distintas diferencias de atributos totales y
muestra una tabla resumen de victorias, empates, derrotas, % de victoria y
goles medios por bando.
"""

from __future__ import annotations

import argparse
import random

from .ai import AutomaticPlayerAI
from .engine import RulesEngine
from .game_state import MatchResult, Team


def _simulate(
    engine: RulesEngine,
    player: Team,
    opponent: Team,
    matches: int,
    base_seed: int,
) -> tuple[int, int, int, int, int]:
    """Ejecuta ``matches`` partidos y devuelve V/E/D y goles totales."""

    rng = random.Random(base_seed)
    wins = draws = losses = 0
    total_goals = 0
    total_bot_goals = 0
    for _ in range(matches):
        seed = rng.randrange(2**63)
        state = engine.create_match_state(player, opponent, random.Random(seed))
        result: MatchResult = engine.play_match(state, AutomaticPlayerAI(engine))
        bot_goals = result.bot_goals
        total_goals += result.player_goals
        total_bot_goals += bot_goals
        if result.player_goals > bot_goals:
            wins += 1
        elif bot_goals > result.player_goals:
            losses += 1
        else:
            draws += 1
    return wins, draws, losses, total_goals, total_bot_goals


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Tabla de equilibrio: V/E/D, % de victoria y goles medios según la diferencia de atributos."
    )
    parser.add_argument("--matches", type=int, default=100, help="Partidos a simular por cada nivel de atributos.")
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
    parser.add_argument("--seed", type=int, default=1, help="Semilla base reproducible.")
    args = parser.parse_args()

    engine = RulesEngine()
    opponent = Team(*args.bot)
    opponent_total = opponent.defense + opponent.midfield + opponent.attack

    print("=" * 88)
    print("      BG FÚTBOL — Informe de equilibrio por diferencia de atributos")
    print("=" * 88)
    print(
        f"Bot fijo: {opponent.defense}/{opponent.midfield}/{opponent.attack}"
        f"  ·  Partidos por nivel: {args.matches}  ·  Semilla base: {args.seed}"
    )
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
    )
    widths = (12, 20, 11, 9, 10, 12, 15, 10)
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

        wins, draws, losses, total_goals, total_bot_goals = _simulate(
            engine, player, opponent, args.matches, args.seed
        )
        win_pct = wins / args.matches * 100
        avg_goals = total_goals / args.matches
        avg_bot_goals = total_bot_goals / args.matches

        row = (
            f"{level}/{level}/{level}",
            gap_label,
            str(wins),
            str(draws),
            str(losses),
            f"{win_pct:.1f}%",
            f"{avg_goals:.2f}",
            f"{avg_bot_goals:.2f}",
        )
        print("".join(value.ljust(width) for value, width in zip(row, widths)))

    print("=" * 88)


if __name__ == "__main__":
    main()
