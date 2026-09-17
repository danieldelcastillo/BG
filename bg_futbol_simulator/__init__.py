"""Simulador del sistema de partido de BG FÚTBOL."""

from .game_state import MatchResult, MatchRules, Team
from .simulation import SimulationConfig, run_simulations

__all__ = [
    "MatchResult",
    "MatchRules",
    "SimulationConfig",
    "Team",
    "run_simulations",
]
