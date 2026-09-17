"""Agregación de resultados de partidos simulados."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

from .game_state import MatchResult


@dataclass(slots=True)
class SimulationStatistics:
    """Métricas acumulables y serializables de una tanda de simulaciones."""

    matches: int = 0
    total_goals: int = 0
    total_bot_goals_from_pressure: int = 0
    total_bot_goals_from_red_cards: int = 0
    total_yellow_cards: int = 0
    total_red_cards: int = 0
    total_player_yellow_cards: int = 0
    total_player_red_cards: int = 0
    total_cr_draws: int = 0
    total_injury_substitutions: int = 0
    total_events: int = 0
    total_final_pressure: int = 0
    total_control_cards_left: int = 0
    total_finalizations: int = 0
    outcome_counts: Counter[str] = field(default_factory=Counter)

    def record(self, result: MatchResult) -> None:
        """Incorpora un resultado de partido."""

        self.matches += 1
        self.total_goals += result.player_goals
        self.total_bot_goals_from_pressure += result.bot_goals_from_pressure
        self.total_bot_goals_from_red_cards += result.bot_goals_from_red_cards
        self.total_yellow_cards += result.yellow_cards
        self.total_red_cards += result.red_cards
        self.total_player_yellow_cards += result.player_yellow_cards
        self.total_player_red_cards += result.player_red_cards
        self.total_cr_draws += result.cr_draws
        self.total_injury_substitutions += result.injury_substitutions
        self.total_events += len(result.events_resolved)
        self.total_final_pressure += result.final_pressure
        self.total_control_cards_left += result.control_cards_left
        self.total_finalizations += result.finalization_count
        for resolution in result.finalizations:
            self.outcome_counts[
                f"{resolution.card_name} :: {resolution.outcome_name}"
            ] += 1

    def merge(self, other: "SimulationStatistics") -> None:
        """Fusiona una tanda independiente, también de procesos distintos."""

        self.matches += other.matches
        self.total_goals += other.total_goals
        self.total_bot_goals_from_pressure += other.total_bot_goals_from_pressure
        self.total_bot_goals_from_red_cards += other.total_bot_goals_from_red_cards
        self.total_yellow_cards += other.total_yellow_cards
        self.total_red_cards += other.total_red_cards
        self.total_player_yellow_cards += other.total_player_yellow_cards
        self.total_player_red_cards += other.total_player_red_cards
        self.total_cr_draws += other.total_cr_draws
        self.total_injury_substitutions += other.total_injury_substitutions
        self.total_events += other.total_events
        self.total_final_pressure += other.total_final_pressure
        self.total_control_cards_left += other.total_control_cards_left
        self.total_finalizations += other.total_finalizations
        self.outcome_counts.update(other.outcome_counts)

    def as_dict(self) -> dict[str, object]:
        """Representación apta para JSON, con tasas derivadas."""

        denominator = self.matches or 1
        total_bot_goals = self.total_bot_goals_from_pressure + self.total_bot_goals_from_red_cards
        return {
            "matches": self.matches,
            "total_player_goals": self.total_goals,
            "player_goals_per_match": self.total_goals / denominator,
            "total_goals": self.total_goals,
            "goals_per_match": self.total_goals / denominator,
            "total_bot_goals": total_bot_goals,
            "bot_goals_per_match": total_bot_goals / denominator,
            "bot_goals_from_pressure": self.total_bot_goals_from_pressure,
            "bot_goals_from_cr": self.total_bot_goals_from_red_cards,
            "total_yellow_cards": self.total_yellow_cards,
            "yellow_cards_per_match": self.total_yellow_cards / denominator,
            "total_red_cards": self.total_red_cards,
            "red_cards_per_match": self.total_red_cards / denominator,
            "total_player_yellow_cards": self.total_player_yellow_cards,
            "player_yellow_cards_per_match": self.total_player_yellow_cards / denominator,
            "total_player_red_cards": self.total_player_red_cards,
            "player_red_cards_per_match": self.total_player_red_cards / denominator,
            "total_cr_draws": self.total_cr_draws,
            "cr_draws_per_match": self.total_cr_draws / denominator,
            "total_injury_substitutions": self.total_injury_substitutions,
            "injury_substitutions_per_match": self.total_injury_substitutions / denominator,
            "mean_events": self.total_events / denominator,
            "mean_final_pressure": self.total_final_pressure / denominator,
            "mean_control_cards_left": self.total_control_cards_left / denominator,
            "mean_finalizations": self.total_finalizations / denominator,
            "outcomes": dict(sorted(self.outcome_counts.items())),
        }
