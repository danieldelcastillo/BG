from __future__ import annotations

import unittest

from bg_futbol_simulator.ai import AutomaticPlayerAI
from bg_futbol_simulator.cards import CardInstance, card_catalogue
from bg_futbol_simulator.engine import RulesEngine
from bg_futbol_simulator.game_state import MatchRules, MatchState, Team


def _instance(definition_id: str, copy_number: int = 1) -> CardInstance:
    return CardInstance(f"test-{definition_id}-{copy_number}", card_catalogue()[definition_id])


class DecisionTreeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = RulesEngine()
        self.ai = AutomaticPlayerAI(self.engine)

    def _state(self, player: Team = Team(15, 15, 15), opponent: Team = Team(15, 15, 15)) -> MatchState:
        return MatchState(player=player, opponent=opponent, rules=MatchRules(), deck=[])

    def test_ai_finds_a_high_result_using_multiple_cards_in_order(self) -> None:
        state = self._state(player=Team(15, 15, 20))
        state.hand = [
            _instance("through_ball"),
            _instance("individual_action"),
        ]
        finalization = card_catalogue()["one_on_one"]

        plan = self.ai.choose_control_plan(state, finalization)

        self.assertEqual(2, plan.cards_spent)
        self.engine.execute_control_plan(state, plan)
        self.assertEqual(2, self.engine.evaluate_finalization(state, finalization).resolution.tier)

    def test_ai_preserves_cards_when_best_result_is_already_available(self) -> None:
        state = self._state(player=Team(15, 15, 20))
        state.hand = [_instance("through_ball")]

        plan = self.ai.choose_control_plan(state, card_catalogue()["one_on_one"])

        self.assertEqual(0, plan.cards_spent)

    def test_ai_does_not_spend_when_no_intermediate_result_is_reachable(self) -> None:
        state = self._state(player=Team(1, 1, 1), opponent=Team(30, 30, 30))
        state.hand = [_instance("through_ball")]

        plan = self.ai.choose_control_plan(state, card_catalogue()["one_on_one"])

        self.assertEqual(0, plan.cards_spent)

    def test_ai_spends_control_to_turn_high_finalization_into_pressure_goal(self) -> None:
        state = self._state(player=Team(15, 18, 26))
        state.pressure = 7
        state.hand = [_instance("game_control")]
        finalization = card_catalogue()["one_on_one"]

        plan = self.ai.choose_control_plan(state, finalization)

        self.assertEqual((("game_control", "comparison_1"),), tuple(
            (play.card_definition_id, play.option_key) for play in plan.plays
        ))
        self.engine.execute_control_plan(state, plan)
        self.engine.resolve_finalization(state, CardInstance("test-one-on-one", finalization))
        self.assertEqual(1, state.player_goals)
        self.assertEqual(5, state.pressure)

    def test_ai_keeps_controls_when_no_plan_can_avoid_bot_pressure_goal(self) -> None:
        state = self._state(player=Team(1, 1, 1), opponent=Team(30, 30, 30))
        state.pressure = 9
        state.hand = [_instance("build_from_back")]

        plan = self.ai.choose_control_plan(state, card_catalogue()["draw_foul"])

        self.assertEqual(0, plan.cards_spent)

    def test_ai_keeps_controls_when_high_finalization_already_scores_by_pressure(self) -> None:
        state = self._state(player=Team(15, 18, 26))
        state.pressure = 5
        state.hand = [_instance("game_control")]

        plan = self.ai.choose_control_plan(state, card_catalogue()["one_on_one"])

        self.assertEqual(0, plan.cards_spent)
