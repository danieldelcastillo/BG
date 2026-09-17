from __future__ import annotations

import unittest

from bg_futbol_simulator.ai import AutomaticPlayerAI
from bg_futbol_simulator.cards import CardInstance, card_catalogue
from bg_futbol_simulator.engine import RulesEngine
from bg_futbol_simulator.game_state import MatchRules, MatchState, Team


def _instance(definition_id: str, copy_number: int = 1) -> CardInstance:
    return CardInstance(f"test-{definition_id}-{copy_number}", card_catalogue()[definition_id])


class HandManagementTests(unittest.TestCase):
    def test_assessment_identifies_duplicate_cards(self) -> None:
        engine = RulesEngine()
        ai = AutomaticPlayerAI(engine)
        state = MatchState(
            player=Team(15, 15, 15),
            opponent=Team(15, 15, 15),
            rules=MatchRules(),
            deck=[],
            hand=[_instance("wing_play", 1), _instance("wing_play", 2), _instance("game_control")],
        )

        assessments = {item.definition_id: item for item in ai.assess_hand(state)}

        self.assertEqual(2, assessments["wing_play"].copies_in_hand)
        self.assertEqual(1, assessments["game_control"].copies_in_hand)
        self.assertIn(ai.choose_control_discard(state), assessments)
