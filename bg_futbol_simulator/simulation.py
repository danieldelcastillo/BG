"""Ejecución reproducible de 1 a 1.000.000 de partidos."""

from __future__ import annotations

import random
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, field
from typing import Literal

from .ai import AutomaticPlayerAI
from .engine import RulesEngine
from .game_state import MatchRules, Team
from .statistics import SimulationStatistics
from .strategies import OneNilLowCRAI


@dataclass(frozen=True, slots=True)
class SimulationConfig:
    """Parámetros de una tanda de partidos."""

    matches: int
    player: Team = Team(15, 15, 15)
    opponent: Team = Team(15, 15, 15)
    seed: int | None = None
    workers: int = 1
    rules: MatchRules = field(default_factory=MatchRules)
    strategy: Literal["standard", "one_nil_low_cr"] = "standard"

    def __post_init__(self) -> None:
        if not 1 <= self.matches <= 1_000_000:
            raise ValueError("matches debe estar entre 1 y 1.000.000.")
        if self.workers <= 0:
            raise ValueError("workers debe ser al menos 1.")
        if self.strategy not in ("standard", "one_nil_low_cr"):
            raise ValueError("strategy debe ser 'standard' o 'one_nil_low_cr'.")


def run_simulations(config: SimulationConfig) -> SimulationStatistics:
    """Ejecuta la tanda solicitada.

    El resultado es determinista para la misma configuración, incluida la
    semilla. Con más de un proceso los lotes son independientes y se agregan al
    final; úsalo para tandas grandes en máquinas con varios núcleos.
    """

    worker_count = min(config.workers, config.matches)
    master_rng = random.Random(config.seed)
    counts = _split_count(config.matches, worker_count)
    batch_specs = [
        (
            count,
            master_rng.getrandbits(64),
            config.player,
            config.opponent,
            config.rules,
            config.strategy,
        )
        for count in counts
    ]

    if worker_count == 1:
        return _run_batch(*batch_specs[0])

    statistics = SimulationStatistics()
    with ProcessPoolExecutor(max_workers=worker_count) as executor:
        for batch_statistics in executor.map(_run_batch_from_spec, batch_specs):
            statistics.merge(batch_statistics)
    return statistics


def _split_count(total: int, parts: int) -> tuple[int, ...]:
    base, remainder = divmod(total, parts)
    return tuple(base + (1 if index < remainder else 0) for index in range(parts))


def _run_batch_from_spec(
    spec: tuple[int, int, Team, Team, MatchRules, Literal["standard", "one_nil_low_cr"]]
) -> SimulationStatistics:
    return _run_batch(*spec)


def _run_batch(
    matches: int,
    batch_seed: int,
    player: Team,
    opponent: Team,
    rules: MatchRules,
    strategy: Literal["standard", "one_nil_low_cr"],
) -> SimulationStatistics:
    """Unidad de trabajo independiente y segura para multiproceso."""

    seed_rng = random.Random(batch_seed)
    engine = RulesEngine()
    ai = OneNilLowCRAI(engine) if strategy == "one_nil_low_cr" else AutomaticPlayerAI(engine)
    statistics = SimulationStatistics()
    for _ in range(matches):
        match_rng = random.Random(seed_rng.getrandbits(64))
        state = engine.create_match_state(player, opponent, match_rng, rules)
        statistics.record(engine.play_match(state, ai))
    return statistics
