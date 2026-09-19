from __future__ import annotations

from dataclasses import replace
import unittest

from bg_futbol_simulator.ai import AutomaticPlayerAI
from bg_futbol_simulator.cards import (
    CardInstance,
    ControlCard,
    EventCard,
    Effect,
    FinalizationCard,
    FinalizationConditional,
    RivalCondition,
    build_match_deck,
    card_catalogue,
)
from bg_futbol_simulator.engine import RulesEngine
from bg_futbol_simulator.game_state import ControlPlay, MatchRules, MatchState, Team


def _state(player: Team = Team(15, 15, 15), opponent: Team = Team(15, 15, 15)) -> MatchState:
    return MatchState(player=player, opponent=opponent, rules=MatchRules(), deck=[])


def _instance(definition_id: str, copy_number: int = 1) -> CardInstance:
    return CardInstance(f"test-{definition_id}-{copy_number}", card_catalogue()[definition_id])


def _finalization_with_conditional(
    definition_id: str, condition: RivalCondition, effect: Effect
) -> CardInstance:
    base_card = card_catalogue()[definition_id]
    assert isinstance(base_card, FinalizationCard)
    conditional = FinalizationConditional(
        label=f"Si {condition.value}",
        condition=condition,
        effect=effect,
    )
    card = replace(base_card, conditional=conditional)
    return CardInstance(f"test-{definition_id}-conditional", card)


class _FirstOptionAI:
    """IA mínima para comprobar un efecto concreto de una CE."""

    def choose_event_option(self, state: MatchState, event: EventCard):
        return event.options[0]

    def choose_control_discard(self, state: MatchState) -> str:
        return state.hand[0].card.definition_id


class CardCatalogueTests(unittest.TestCase):
    def test_definitive_deck_has_28_cc_12_cf_and_10_ce(self) -> None:
        deck = build_match_deck()
        self.assertEqual(50, len(deck))
        self.assertEqual(28, sum(isinstance(instance.card, ControlCard) for instance in deck))
        self.assertEqual(12, sum(isinstance(instance.card, FinalizationCard) for instance in deck))
        self.assertEqual(10, sum(isinstance(instance.card, EventCard) for instance in deck))

    def test_every_control_card_has_exactly_three_exclusive_options(self) -> None:
        for card in card_catalogue().values():
            if isinstance(card, ControlCard) and card.definition_id != "fuerza_del_debil":
                self.assertEqual(
                    ("base", "comparison_1", "comparison_2"),
                    tuple(option.key for option in card.options),
                )

    def test_weak_team_support_card_has_two_unconditional_options(self) -> None:
        card = card_catalogue()["fuerza_del_debil"]
        self.assertIsInstance(card, ControlCard)
        self.assertEqual(("option_1", "option_2"), tuple(option.key for option in card.options))
        self.assertTrue(all(option.comparison is None for option in card.options))


class EngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = RulesEngine()

    def test_cc_bonus_is_consumed_by_the_next_control_card(self) -> None:
        state = _state()
        state.hand = [
            _instance("build_from_back"),
            _instance("wing_play"),
            _instance("aggressive_recovery"),
        ]

        self.engine.apply_control_play(state, ControlPlay("build_from_back", "base"))
        self.assertEqual(1, state.pending_cc_bonus)

        # MED 15 + el bono +CC supera MED 15 + 1. La recompensa genera un
        # nuevo +CC para la siguiente carta, no conserva el anterior.
        self.engine.apply_control_play(state, ControlPlay("wing_play", "comparison_2"))
        self.assertEqual(1, state.pending_cc_bonus)

        self.engine.apply_control_play(state, ControlPlay("aggressive_recovery", "base"))
        self.assertEqual(0, state.pending_cc_bonus)

    def test_cf_bonus_accumulates_and_is_consumed_on_resolution(self) -> None:
        state = _state()
        state.pending_cf_bonus = 9
        finalization = _instance("one_on_one")
        resolution = self.engine.resolve_finalization(state, finalization)

        self.assertEqual(2, resolution.tier)
        self.assertEqual(1, state.player_goals)
        self.assertEqual(0, state.pending_cf_bonus)

    def test_updated_finalization_comparisons_are_strict(self) -> None:
        state = _state()
        one_on_one = _instance("one_on_one")

        # AT 15 no supera estrictamente DEF 15: se llega al fallo.
        self.assertEqual(
            "Roba 1 CR",
            self.engine.evaluate_finalization(state, one_on_one.card).resolution.outcome_name,
        )

        state.pending_cf_bonus = 1
        self.assertEqual(
            "+1 Presión",
            self.engine.evaluate_finalization(state, one_on_one.card).resolution.outcome_name,
        )

    def test_cf_conditional_is_applied_independently_when_rival_is_winning(self) -> None:
        state = _state(player=Team(1, 1, 1), opponent=Team(30, 30, 30))
        state.bot_goals_from_pressure = 1
        finalization = _finalization_with_conditional(
            "one_on_one",
            RivalCondition.RIVAL_WINNING,
            Effect(pressure_delta=2),
        )

        resolution = self.engine.resolve_finalization(state, finalization)

        # El resultado principal sigue aplicándose y el condicional de la CF
        # se suma de forma independiente cuando el rival va ganando.
        self.assertEqual("Roba 1 CR", resolution.outcome_name)
        self.assertEqual(1, state.cr_draws)
        self.assertEqual(2, state.pressure)
        self.assertIn("cf_condicional", [event.kind for event in state.events])


    def test_cf_conditional_executes_before_primary_effect(self) -> None:
        state = _state(player=Team(15, 15, 15), opponent=Team(15, 15, 16))
        state.bot_goals_from_pressure = 1
        state.pressure = 7
        finalization = _finalization_with_conditional(
            "one_on_one",
            RivalCondition.RIVAL_WINNING,
            Effect(pressure_delta=-4),
        )

        resolution = self.engine.resolve_finalization(state, finalization)

        # Primero baja 4 la presión (7 -> 3) y después el resultado principal
        # añade 4 (3 -> 7). Si se ejecutara al revés, el +4 provocaría un gol
        # del bot y la presión terminaría en 0.
        self.assertEqual(
            "Descarta 1 CC de la mano y +4 Presión",
            resolution.outcome_name,
        )
        self.assertEqual(7, state.pressure)
        self.assertEqual(1, state.bot_goals_from_pressure)
        kinds = [event.kind for event in state.events]
        self.assertLess(kinds.index("cf_condicional"), kinds.index("resuelve_cf"))

    def test_cr_conditional_executes_before_primary_action(self) -> None:
        from bg_futbol_simulator.cards import RedCard, RedCardConditional, red_card_catalogue

        state = _state(player=Team(15, 15, 15), opponent=Team(15, 19, 15))
        state.bot_goals_from_pressure = 1
        state.pressure = 5
        base_card = red_card_catalogue()["ataque_banda"]
        self.assertIsInstance(base_card, RedCard)
        conditional = RedCardConditional(
            label="Si el rival está ganando",
            condition=RivalCondition.RIVAL_WINNING,
            effect=Effect(pressure_delta=-4),
        )
        card = replace(base_card, conditional=conditional)
        instance = CardInstance("test-ataque-banda-precondicional", card)

        self.engine.resolve_red_card(state, instance)

        # Primero 5 -> 1 por el condicional y luego +7 por la acción principal:
        # el resultado es 8. Al revés, 5 -> 12 provocaría gol del bot y después
        # la presión bajaría a 0.
        self.assertEqual(8, state.pressure)
        self.assertEqual(1, state.bot_goals_from_pressure)
        kinds = [event.kind for event in state.events]
        self.assertLess(kinds.index("cr_condicion"), kinds.index("cr_accion"))

    def test_cf_conditional_is_not_applied_when_its_score_condition_is_false(self) -> None:
        state = _state(player=Team(1, 1, 1), opponent=Team(30, 30, 30))
        finalization = _finalization_with_conditional(
            "one_on_one",
            RivalCondition.RIVAL_WINNING,
            Effect(pressure_delta=2),
        )

        resolution = self.engine.resolve_finalization(state, finalization)

        self.assertEqual("Roba 1 CR", resolution.outcome_name)
        self.assertEqual(1, state.cr_draws)
        self.assertEqual(0, state.pressure)
        self.assertNotIn("cf_condicional", [event.kind for event in state.events])

    def test_cf_conditional_can_use_rival_losing_condition(self) -> None:
        state = _state(player=Team(1, 1, 1), opponent=Team(30, 30, 30))
        state.player_goals = 1
        finalization = _finalization_with_conditional(
            "one_on_one",
            RivalCondition.RIVAL_LOSING,
            Effect(pressure_delta=3),
        )

        self.engine.resolve_finalization(state, finalization)

        self.assertEqual(3, state.pressure)
        self.assertIn("cf_condicional", [event.kind for event in state.events])

    def test_updated_cutback_uses_midfield(self) -> None:
        state = _state(player=Team(15, 21, 99))
        cutback = _instance("cutback")

        self.assertEqual(
            "Gol",
            self.engine.evaluate_finalization(state, cutback.card).resolution.outcome_name,
        )

    def test_top_deck_discard_skips_card_effects(self) -> None:
        state = _state()
        discarded = _instance("one_on_one")
        state.deck = [discarded]
        state.hand = [_instance("switch_of_play")]

        self.engine.apply_control_play(state, ControlPlay("switch_of_play", "base"))

        self.assertEqual([], state.deck)
        self.assertIn(discarded, state.discard_pile)
        self.assertEqual([], state.finalizations)

    def test_exceeding_pressure_nine_gives_bot_a_goal_and_resets_pressure(self) -> None:
        state = _state()
        state.pressure = 9
        state.hand = [_instance("through_ball")]

        self.engine.apply_control_play(state, ControlPlay("through_ball", "base"))

        self.assertEqual(0, state.pressure)
        self.assertEqual(1, state.bot_goals_from_pressure)

    def test_sixth_control_card_forces_a_hand_discard(self) -> None:
        state = _state()
        state.deck = [
            _instance("wing_play", 1),
            _instance("wing_play", 2),
            _instance("through_ball"),
            _instance("individual_action"),
            _instance("build_from_back"),
            _instance("game_control"),
        ]

        self.engine.play_match(state, AutomaticPlayerAI(self.engine))

        self.assertEqual(5, len(state.hand))
        self.assertEqual(1, len(state.discard_pile))
        self.assertEqual("descarte_mano_cc", state.events[-1].kind)

    def test_event_is_resolved_as_a_player_choice(self) -> None:
        state = _state()
        state.deck = [_instance("offside")]

        self.engine.play_match(state, AutomaticPlayerAI(self.engine))

        self.assertEqual(1, len(state.events_resolved))
        self.assertEqual("Fuera de juego", state.events_resolved[0].card_name)
        self.assertEqual(1, state.cr_draws)

    def test_offside_option_one_discards_deck_card_and_control_from_hand(self) -> None:
        state = _state()
        deck_card = _instance("one_on_one")
        hand_card = _instance("individual_action")
        state.deck = [deck_card]
        state.hand = [hand_card]

        self.engine.resolve_event(state, _instance("offside"), _FirstOptionAI())

        self.assertEqual([], state.deck)
        self.assertEqual([], state.hand)
        self.assertIn(deck_card, state.discard_pile)
        self.assertIn(hand_card, state.discard_pile)
