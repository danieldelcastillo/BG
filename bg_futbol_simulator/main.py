"""Interfaz de línea de comandos para simulaciones de BG FÚTBOL."""

from __future__ import annotations

import argparse
import json

from .game_state import Team
from .simulation import SimulationConfig, run_simulations


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simulador de partido de BG FÚTBOL")
    parser.add_argument("--matches", type=int, default=100, help="Partidos a simular (1–1.000.000).")
    parser.add_argument("--seed", type=int, default=20260719, help="Semilla reproducible.")
    parser.add_argument("--workers", type=int, default=1, help="Procesos de simulación.")
    for prefix, label in (("player", "jugador"), ("opponent", "rival")):
        parser.add_argument(f"--{prefix}-def", type=int, default=15, help=f"DEF del {label}.")
        parser.add_argument(f"--{prefix}-med", type=int, default=15, help=f"MED del {label}.")
        parser.add_argument(f"--{prefix}-at", type=int, default=15, help=f"AT del {label}.")
    return parser


def main() -> None:
    """Ejecuta la CLI y emite métricas en JSON."""

    args = _parser().parse_args()
    config = SimulationConfig(
        matches=args.matches,
        seed=args.seed,
        workers=args.workers,
        player=Team(args.player_def, args.player_med, args.player_at),
        opponent=Team(args.opponent_def, args.opponent_med, args.opponent_at),
    )
    print(json.dumps(run_simulations(config).as_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
