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
    red_card_catalogue,
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
        self.assertEqual(3, state.pending_cc_bonus)

        # MED 15 + el bono +CC supera MED 15 + 1. La recompensa genera un
        # nuevo +CC para la siguiente carta, no conserva el anterior.
        self.engine.apply_control_play(state, ControlPlay("wing_play", "comparison_2"))
        self.assertEqual(11, state.pending_cc_bonus)

        self.engine.apply_control_play(state, ControlPlay("aggressive_recovery", "base"))
        self.assertEqual(4, state.pending_cc_bonus)

    def test_cf_bonus_accumulates_and_is_consumed_on_resolution(self) -> None:
        state = _state()
        state.pending_cf_bonus = 9
        finalization = _instance("one_on_one")
        resolution = self.engine.resolve_finalization(state, finalization)

        self.assertEqual(1, resolution.tier)
        self.assertEqual(0, state.player_goals)
        self.assertEqual(0, state.pending_cf_bonus)

    def test_updated_finalization_comparisons_are_strict(self) -> None:
        state = _state(player=Team(15, 15, 14))
        one_on_one = _instance("one_on_one")

        # AT 14 no supera estrictamente DEF 15 - 1: se llega al fallo.
        self.assertEqual(
            "Roba 1 CR",
            self.engine.evaluate_finalization(state, one_on_one.card).resolution.outcome_name,
        )

        state.pending_cf_bonus = 1
        self.assertEqual(
            "Descarta 1 CC de la mano y +1 Presión",
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
        self.assertEqual(7, state.pressure)
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
        # añade 1 (3 -> 4). El orden se registra antes de resolver la CF.
        self.assertEqual(
            "Descarta 1 CC de la mano y +1 Presión",
            resolution.outcome_name,
        )
        self.assertEqual(4, state.pressure)
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

        # Primero 5 -> 1 por el condicional y luego +4 por la acción principal:
        # el resultado es 5. El condicional siempre se resuelve antes de las
        # comparaciones y de la acción principal.
        self.assertEqual(5, state.pressure)
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
        self.assertEqual(5, state.pressure)
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

        self.assertEqual(8, state.pressure)
        self.assertIn("cf_condicional", [event.kind for event in state.events])

    def test_updated_cutback_uses_midfield(self) -> None:
        state = _state(player=Team(15, 21, 99))
        cutback = _instance("cutback")

        self.assertEqual(
            "+2 Presión",
            self.engine.evaluate_finalization(state, cutback.card).resolution.outcome_name,
        )

    def test_long_shot_default_draws_a_red_card_without_discarding_control(self) -> None:
        state = _state(player=Team(15, 15, 13))
        kept_control = _instance("individual_action")
        state.hand = [kept_control]

        resolution = self.engine.resolve_finalization(state, _instance("long_shot"))

        self.assertEqual("Roba 1 CR", resolution.outcome_name)
        self.assertEqual(1, state.cr_draws)
        self.assertEqual([kept_control], state.hand)

    def test_long_shot_intermediate_adds_pressure_and_discards_control(self) -> None:
        state = _state(player=Team(15, 15, 14))
        discarded_control = _instance("individual_action")
        state.hand = [discarded_control]

        resolution = self.engine.resolve_finalization(state, _instance("long_shot"))

        self.assertEqual("+2 Presión y descarta una CC", resolution.outcome_name)
        self.assertEqual(7, state.pressure)
        self.assertEqual([], state.hand)
        self.assertIn(discarded_control, state.discard_pile)

    def test_midfield_theft_red_card_uses_the_updated_effects(self) -> None:
        card = red_card_catalogue()["robo_mediocampo"]

        self.assertEqual(5, card.actions[0].effect.pressure_delta)
        self.assertEqual(0, card.actions[0].effect.discard_control_cards)
        self.assertEqual(4, card.actions[1].effect.pressure_delta)
        self.assertEqual(4, card.fallback_effect.pressure_delta)
        self.assertEqual(1, card.fallback_effect.discard_control_cards)

    def test_intercepted_pass_first_red_card_action_adds_pressure_and_discards_control(self) -> None:
        card = red_card_catalogue()["pase_cortado"]
        effect = card.actions[0].effect

        self.assertEqual(4, effect.pressure_delta)
        self.assertEqual(1, effect.discard_control_cards)
        self.assertEqual(0, effect.recover_control_cards)

    def test_updated_pressure_effects_for_corner_red_cards_and_time_wasting(self) -> None:
        corner = card_catalogue()["win_corner"]
        self.assertEqual("-4 Presión", corner.outcomes[0].name)
        self.assertEqual(-4, corner.outcomes[0].effect.pressure_delta)

        for definition_id in ("accion_individual_rival", "balon_parado"):
            effect = red_card_catalogue()[definition_id].actions[0].effect
            self.assertEqual(6, effect.pressure_delta)
            self.assertEqual(0, effect.bot_goals)

        time_wasting = card_catalogue()["time_wasting"]
        self.assertEqual(-3, time_wasting.options[2].effect.pressure_delta)

    def test_game_control_comparison_options_use_the_mitigated_pressure_cost(self) -> None:
        card = card_catalogue()["game_control"]

        self.assertEqual(-2, card.options[1].effect.pressure_delta)
        self.assertEqual(9, card.options[1].effect.cc_bonus)
        self.assertEqual(-2, card.options[2].effect.pressure_delta)
        self.assertEqual(7, card.options[2].effect.cc_bonus)

    def test_top_deck_discard_skips_card_effects(self) -> None:
        state = _state()
        discarded = _instance("one_on_one")
        state.deck = [discarded]
        state.hand = [_instance("switch_of_play")]

        self.engine.apply_control_play(state, ControlPlay("switch_of_play", "base"))

        self.assertEqual([], state.deck)
        self.assertIn(discarded, state.discard_pile)
        self.assertEqual([], state.finalizations)

    def test_reaching_pressure_ten_gives_bot_a_goal_and_resets_pressure(self) -> None:
        state = _state()
        state.pressure = 9
        state.hand = [_instance("through_ball")]

        self.engine.apply_control_play(state, ControlPlay("through_ball", "base"))

        self.assertEqual(5, state.pressure)
        self.assertEqual(1, state.bot_goals_from_pressure)

    def test_reaching_pressure_zero_gives_player_a_goal_and_resets_pressure(self) -> None:
        state = _state()
        state.pressure = 5

        self.engine.apply_effect(state, Effect(pressure_delta=-5))

        self.assertEqual(5, state.pressure)
        self.assertEqual(1, state.player_goals)

    def test_high_finalization_reduces_pressure_instead_of_scoring_directly(self) -> None:
        state = _state(player=Team(15, 15, 26))

        resolution = self.engine.resolve_finalization(state, _instance("one_on_one"))

        self.assertEqual("-5 Presión", resolution.outcome_name)
        self.assertEqual(5, state.pressure)
        self.assertEqual(1, state.player_goals)

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

    def test_event_ai_prefers_option_that_reaches_zero_pressure(self) -> None:
        state = _state()
        state.pressure = 2
        event = card_catalogue()["time_wasting"]
        self.assertIsInstance(event, EventCard)

        option = AutomaticPlayerAI(self.engine).choose_event_option(state, event)

        _, player_goal, bot_goal = self.engine.pressure_after_delta(
            state.rules, state.pressure, option.effect.pressure_delta
        )
        self.assertTrue(player_goal)
        self.assertFalse(bot_goal)

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
