from __future__ import annotations

import unittest

from bg_futbol_simulator.cards import CardInstance, card_catalogue
from bg_futbol_simulator.engine import RulesEngine
from bg_futbol_simulator.game_state import MatchRules, MatchState, Team
from bg_futbol_simulator.strategies import OneNilLowCRAI


class OneNilStrategyTests(unittest.TestCase):
    def test_before_two_cr_keeps_controls_when_they_cannot_score(self) -> None:
        engine = RulesEngine()
        state = MatchState(
            player=Team(15, 15, 15),
            opponent=Team(15, 15, 15),
            rules=MatchRules(),
            deck=[],
            hand=[CardInstance("individual", card_catalogue()["individual_action"])],
        )

        plan = OneNilLowCRAI(engine).choose_control_plan(
            state, card_catalogue()["one_on_one"]
        )

        # +1 CF evita la CR, pero no alcanza el gol: se guarda para después.
        self.assertEqual(0, plan.cards_spent)

    def test_from_two_cr_prefers_avoiding_another_cr_to_saving_cards(self) -> None:
        engine = RulesEngine()
        state = MatchState(
            player=Team(15, 15, 15),
            opponent=Team(15, 15, 15),
            rules=MatchRules(),
            deck=[],
            cr_draws=2,
            hand=[CardInstance("individual", card_catalogue()["individual_action"])],
        )
        finalization = card_catalogue()["one_on_one"]

        plan = OneNilLowCRAI(engine).choose_control_plan(state, finalization)
        engine.execute_control_plan(state, plan)
        preview = engine.evaluate_finalization(state, finalization)

        self.assertEqual(1, plan.cards_spent)
        self.assertEqual("+1 Presión", preview.resolution.outcome_name)
        self.assertEqual(0, preview.outcome.effect.cr_draws)

    def test_after_first_goal_strategy_avoids_cr_without_scoring_again(self) -> None:
        engine = RulesEngine()
        state = MatchState(
            player=Team(15, 15, 15),
            opponent=Team(15, 15, 15),
            rules=MatchRules(),
            deck=[],
            player_goals=1,
            hand=[CardInstance("individual", card_catalogue()["individual_action"])],
        )
        finalization = card_catalogue()["one_on_one"]

        plan = OneNilLowCRAI(engine).choose_control_plan(state, finalization)
        engine.execute_control_plan(state, plan)
        preview = engine.evaluate_finalization(state, finalization)

        self.assertEqual(1, plan.cards_spent)
        self.assertEqual("+1 Presión", preview.resolution.outcome_name)
        self.assertEqual(0, preview.outcome.effect.goals)
        self.assertEqual(0, preview.outcome.effect.cr_draws)
