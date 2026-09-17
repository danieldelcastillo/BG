"""Asistente interactivo para crear informes de un partido de BG FÚTBOL."""

from __future__ import annotations

from datetime import datetime
import os
from pathlib import Path
import subprocess
import sys
from typing import TextIO

from .game_state import Team
from .simulation import SimulationConfig, run_simulations
from .statistics import SimulationStatistics
from .trace import write_match_trace


def _ask_nonnegative(prompt: str) -> int:
    """Solicita un atributo válido sin cerrar el asistente ante un error."""

    while True:
        try:
            value = int(input(prompt).strip())
        except ValueError:
            print("  Escribe un número entero, por ejemplo 15.")
            continue
        if value < 0:
            print("  El atributo no puede ser negativo.")
            continue
        return value


def _ask_team(label: str) -> Team:
    print(f"\nAtributos de {label}:")
    return Team(
        defense=_ask_nonnegative("  DEF: "),
        midfield=_ask_nonnegative("  MED: "),
        attack=_ask_nonnegative("  AT: "),
    )


def _ask_strategy() -> tuple[str, str]:
    """Devuelve el identificador interno y el texto del estilo elegido."""

    while True:
        print("\nEstilo de juego:")
        print("  1. Buscar 1–0 y recibir las menores CR posibles")
        print("  2. Juego agresivo: buscar el mejor resultado de cada CF")
        choice = input("Elige 1 o 2 [1]: ").strip() or "1"
        if choice == "1":
            return "one_nil_low_cr", "1–0 y pocas CR"
        if choice == "2":
            return "standard", "agresivo"
        print("  Elige 1 o 2.")


def _ask_match_count() -> int:
    """Pregunta cuántos partidos se quieren ejecutar en el informe."""

    while True:
        text = input("\nNúmero de simulaciones [1]: ").strip()
        if not text:
            return 1
        try:
            count = int(text)
        except ValueError:
            print("  Escribe un número entero, por ejemplo 100.")
            continue
        if count < 0:
            print("  El número de simulaciones no puede ser negativo.")
            continue
        if count == 0:
            print("  Debe ser al menos 1.")
            continue
        if count > 1_000_000:
            print("  El máximo es 1.000.000 de simulaciones.")
            continue
        return count


def _ask_seed() -> int:
    """Permite repetir un partido o deja una semilla nueva por defecto."""

    while True:
        text = input("Semilla (Enter para una simulación nueva): ").strip()
        if not text:
            return int.from_bytes(os.urandom(8), "big")
        try:
            return int(text)
        except ValueError:
            print("  La semilla debe ser un número entero o puedes dejarla vacía.")


def _report_path(reports_dir: Path, prefix: str) -> Path:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return reports_dir / f"{prefix}_{timestamp}.md"


def _write_summary_report(
    output: TextIO,
    statistics: SimulationStatistics,
    player: Team,
    opponent: Team,
    strategy_label: str,
) -> None:
    """Escribe un resumen de tanda sin detallar las cartas de cada partido."""

    matches = statistics.matches
    average = lambda total: total / matches
    total_bot_goals = statistics.total_bot_goals_from_pressure + statistics.total_bot_goals_from_red_cards
    rows = (
        ("Goles del jugador", statistics.total_goals),
        ("Goles del bot por presión", statistics.total_bot_goals_from_pressure),
        ("Goles del bot por CR", statistics.total_bot_goals_from_red_cards),
        ("CR robadas", statistics.total_cr_draws),
        ("🟨 Amarillas al rival", statistics.total_yellow_cards),
        ("🟥 Rojas al rival", statistics.total_red_cards),
        ("🟨 Amarillas propias", statistics.total_player_yellow_cards),
        ("🟥 Rojas propias", statistics.total_player_red_cards),
        ("Sustituciones por lesión", statistics.total_injury_substitutions),
        ("CE resueltas", statistics.total_events),
        ("CF resueltas", statistics.total_finalizations),
        ("Presión final acumulada", statistics.total_final_pressure),
        ("CC finales en mano", statistics.total_control_cards_left),
    )
    print("# Resumen de simulaciones — BG FÚTBOL", file=output)
    print(file=output)
    print(f"- Partidos simulados: **{matches}**", file=output)
    print(
        f"- Jugador: DEF {player.defense} · MED {player.midfield} · AT {player.attack}",
        file=output,
    )
    print(
        f"- Bot: DEF {opponent.defense} · MED {opponent.midfield} · AT {opponent.attack}",
        file=output,
    )
    print(f"- Estilo: **{strategy_label}**", file=output)
    print(file=output)
    result_icon = (
        "🏆" if statistics.total_goals > total_bot_goals
        else "💔" if total_bot_goals > statistics.total_goals
        else "🤝"
    )
    print(
        f"### {result_icon} Marcador agregado: Jugador {statistics.total_goals} – "
        f"{total_bot_goals} Bot (media {average(statistics.total_goals):.2f} – "
        f"{average(total_bot_goals):.2f} por partido)",
        file=output,
    )
    print(file=output)
    print("## Totales y media por partido", file=output)
    print(file=output)
    print("| Métrica | Total | Media |", file=output)
    print("| --- | ---: | ---: |", file=output)
    for label, total in rows:
        print(f"| {label} | **{total}** | **{average(total):.2f}** |", file=output)


def main() -> None:
    """Muestra el menú, crea el informe y abre su carpeta en el Explorador."""

    print("=" * 58)
    print("      BG FÚTBOL — simulación de un partido")
    print("=" * 58)
    try:
        player = _ask_team("tu equipo")
        opponent = _ask_team("el bot")
        matches = _ask_match_count()
        strategy, strategy_label = _ask_strategy()
        seed = _ask_seed() if matches == 1 else None
    except (EOFError, KeyboardInterrupt):
        print("\nSimulación cancelada.")
        return

    reports_dir = Path.cwd() / "reports"
    reports_dir.mkdir(exist_ok=True)
    output = _report_path(
        reports_dir,
        "partido" if matches == 1 else f"resumen_{matches}_partidos",
    )
    with output.open("w", encoding="utf-8", newline="\n") as stream:
        if matches == 1:
            assert seed is not None
            write_match_trace(
                seed,
                stream,
                strategy=strategy,
                player=player,
                opponent=opponent,
            )
        else:
            statistics = run_simulations(
                SimulationConfig(
                    matches=matches,
                    player=player,
                    opponent=opponent,
                    seed=int.from_bytes(os.urandom(8), "big"),
                    strategy=strategy,
                )
            )
            _write_summary_report(stream, statistics, player, opponent, strategy_label)

    print("\nInforme creado correctamente.")
    print(f"  Equipos: {player.defense}/{player.midfield}/{player.attack} vs "
          f"{opponent.defense}/{opponent.midfield}/{opponent.attack}")
    print(f"  Estilo: {strategy_label}")
    if seed is not None:
        print(f"  Semilla: {seed}")
    print(f"  Archivo: {output}")
    if sys.platform == "win32":
        try:
            # No abrimos el .md directamente: si está asociado a VS Code, sus
            # mensajes técnicos pueden invadir esta consola. El Explorador lo
            # muestra seleccionado para abrirlo con doble clic cuando se desee.
            subprocess.Popen(
                ["explorer.exe", f"/select,{output}"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except OSError:
            print("No se pudo abrir el Explorador; puedes abrir el archivo indicado.")


if __name__ == "__main__":
    main()
