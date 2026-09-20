from __future__ import annotations

import unittest

from .cards import (
    Attribute,
    CardInstance,
    Effect,
    RedCardAction,
    RedComparison,
    RivalCondition,
    _red_card,
    _red_conditional,
)
from .engine import RulesEngine
from .game_state import MatchRules, MatchState, Team


class RedConditionalTemporaryModifierTests(unittest.TestCase):
    def _make_cr(self, *, attribute: Attribute, modifier: int):
        return _red_card(
            "test_cr",
            "CR prueba",
            RedCardAction("Acción 1", RedComparison(attribute, Attribute.DEF, 0), Effect(pressure_delta=1)),
            RedCardAction("Acción 2", RedComparison(attribute, Attribute.DEF, 100), Effect(pressure_delta=2)),
            Effect(pressure_delta=3),
            _red_conditional(
                RivalCondition.RIVAL_WINNING,
                Effect(),
                temporary_opponent_attribute=attribute,
                temporary_opponent_modifier=modifier,
            ),
        )

    def test_modifier_changes_cr_comparison_without_changing_team(self) -> None:
        engine = RulesEngine()
        card = self._make_cr(attribute=Attribute.AT, modifier=2)
        state = MatchState(
            player=Team(15, 15, 15),
            opponent=Team(16, 15, 15),
            rules=MatchRules(),
            deck=[],
            red_deck=[],
            bot_goals_from_pressure=1,
        )
        engine.resolve_red_card(state, CardInstance("test_cr-1", card), log=False)
        resolution = state.red_card_resolutions[0]
        self.assertEqual(0, resolution.applied_action_index)
        self.assertEqual(Attribute.AT, resolution.temporary_opponent_attribute)
        self.assertEqual(2, resolution.temporary_opponent_modifier)
        self.assertEqual(15, state.opponent.value(Attribute.AT))

    def test_modifier_only_affects_matching_opponent_attribute(self) -> None:
        engine = RulesEngine()
        state = MatchState(
            player=Team(15, 15, 15),
            opponent=Team(16, 14, 15),
            rules=MatchRules(),
            deck=[],
        )
        comparison = RedComparison(Attribute.MED, Attribute.DEF, 0)
        self.assertFalse(
            engine.red_comparison_succeeds(
                state, comparison,
                temporary_opponent_attribute=Attribute.AT,
                temporary_opponent_modifier=5,
            )
        )

    def test_modifier_is_not_active_when_condition_fails(self) -> None:
        engine = RulesEngine()
        card = self._make_cr(attribute=Attribute.AT, modifier=2)
        state = MatchState(
            player=Team(15, 15, 15),
            opponent=Team(16, 15, 15),
            rules=MatchRules(),
            deck=[],
        )
        engine.resolve_red_card(state, CardInstance("test_cr-1", card), log=False)
        resolution = state.red_card_resolutions[0]
        self.assertFalse(resolution.conditional_met)
        self.assertIsNone(resolution.temporary_opponent_attribute)
        self.assertEqual(0, resolution.temporary_opponent_modifier)


if __name__ == "__main__":
    unittest.main()
