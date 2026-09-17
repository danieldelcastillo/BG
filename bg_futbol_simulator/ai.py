"""IA automática del jugador para el sistema de partido."""

from __future__ import annotations

from dataclasses import dataclass

from .cards import CardInstance, ControlCard, EventCard, EventOption, FinalizationCard
from .decision_tree import DecisionTree
from .engine import RulesEngine
from .game_state import ControlPlan, MatchState


@dataclass(frozen=True, slots=True)
class HandCardAssessment:
    """Valor estratégico explicable de una CC cuando la mano se llena."""

    definition_id: str
    name: str
    copies_in_hand: int
    usable_comparisons: int
    potentially_usable_comparisons: int
    best_effect_value: int


class AutomaticPlayerAI:
    """Jugador automático que aplica la prioridad indicada por las reglas."""

    def __init__(self, engine: RulesEngine, decision_tree: DecisionTree | None = None) -> None:
        self.engine = engine
        self.decision_tree = decision_tree or DecisionTree(engine)

    def choose_control_plan(
        self, state: MatchState, finalization: FinalizationCard
    ) -> ControlPlan:
        """Encuentra la mejor secuencia de CC para la CF que acaba de aparecer."""

        return self.decision_tree.choose_plan(state, finalization)

    def choose_control_discard(self, state: MatchState) -> str:
        """Elige la CC menos útil al superar el máximo de mano.

        La regla no define una jerarquía numérica de descarte. Esta política
        determinista hace visible el criterio y puede sustituirse sin tocar el
        motor: combina el valor del mejor efecto alcanzable, comparaciones que
        el equipo puede aprovechar y redundancia de copias. En un empate, el id
        estable evita resultados aleatorios.
        """

        assessments = self.assess_hand(state)
        if not assessments:
            raise ValueError("No hay CC en mano para descartar.")
        worst = min(
            assessments,
            key=lambda item: (
                self._retention_score(item),
                0 if item.copies_in_hand > 1 else 1,
                -item.copies_in_hand,
                item.definition_id,
            ),
        )
        return worst.definition_id

    def choose_event_option(self, state: MatchState, event: EventCard) -> EventOption:
        """Elige la opción de CE con mayor valor inmediato para el jugador.

        Las CE son decisiones del jugador. Esta valoración automática premia
        recursos (robo, CR, recuperación), resultados favorables al rival y
        presión baja; penaliza descartes, presión, amarillas propias y lesión.
        """

        return max(
            event.options,
            key=lambda option: (self._event_option_value(state, option), option.key),
        )

    def choose_control_recovery(
        self, state: MatchState, candidates: tuple[CardInstance, ...]
    ) -> str:
        """Recupera del descarte la CC con mejor potencial de uso."""

        scored: list[tuple[int, str]] = []
        for instance in candidates:
            card = instance.card
            assert isinstance(card, ControlCard)
            value = max(self._effect_value(state, option.effect) for option in card.options)
            usable = sum(
                option.comparison is not None
                and self.engine.comparison_succeeds(state, option.comparison, state.pending_cc_bonus)
                for option in card.options
            )
            scored.append((value + int(usable) * 60, card.definition_id))
        return max(scored)[1]

    def assess_hand(self, state: MatchState) -> tuple[HandCardAssessment, ...]:
        """Expone la valoración de cada tipo de CC para auditoría o interfaz."""

        cards: dict[str, ControlCard] = {}
        counts: dict[str, int] = {}
        for instance in state.hand:
            if isinstance(instance.card, ControlCard):
                cards[instance.card.definition_id] = instance.card
                counts[instance.card.definition_id] = counts.get(instance.card.definition_id, 0) + 1

        # El mayor +CC que puede producir una carta del sistema sirve para
        # estimar si una comparación puede aprovecharse tras una preparación.
        future_cc_bonus = max(
            [state.pending_cc_bonus]
            + [
                option.effect.cc_bonus
                for card in cards.values()
                for option in card.options
            ]
        )
        assessments: list[HandCardAssessment] = []
        for definition_id, card in cards.items():
            usable = 0
            potential = 0
            effect_values = [self._effect_value(state, card.options[0].effect)]
            for option in card.options[1:]:
                if option.comparison is None:
                    usable += 1
                    potential += 1
                    effect_values.append(self._effect_value(state, option.effect))
                    continue
                if self.engine.comparison_succeeds(
                    state, option.comparison, state.pending_cc_bonus
                ):
                    usable += 1
                    potential += 1
                    effect_values.append(self._effect_value(state, option.effect))
                elif self.engine.comparison_succeeds(
                    state, option.comparison, future_cc_bonus
                ):
                    potential += 1
                    effect_values.append(self._effect_value(state, option.effect))
            assessments.append(
                HandCardAssessment(
                    definition_id=definition_id,
                    name=card.name,
                    copies_in_hand=counts[definition_id],
                    usable_comparisons=usable,
                    potentially_usable_comparisons=potential,
                    best_effect_value=max(effect_values),
                )
            )
        return tuple(sorted(assessments, key=lambda item: item.definition_id))

    @staticmethod
    def _effect_value(state: MatchState, effect) -> int:
        """Escala común de efectos para ordenar descartes, no para resolver CC."""

        pressure_relief = min(
            state.pressure - state.rules.pressure_floor,
            max(0, -effect.pressure_delta),
        )
        pressure_cost = max(0, effect.pressure_delta)
        return (
            effect.cf_bonus * 100
            + effect.cc_bonus * 40
            + pressure_relief * 15
            - pressure_cost * 15
            - effect.discard_top_cards * 5
        )

    @staticmethod
    def _retention_score(assessment: HandCardAssessment) -> int:
        """Valor compuesto: efecto útil, rendimiento y penalización por copia."""

        return (
            assessment.best_effect_value
            + assessment.usable_comparisons * 60
            + assessment.potentially_usable_comparisons * 20
            - (assessment.copies_in_hand - 1) * 15
        )

    @staticmethod
    def _event_option_value(state: MatchState, option: EventOption) -> int:
        effect = option.effect
        pressure_relief = min(
            state.pressure - state.rules.pressure_floor,
            max(0, -effect.pressure_delta),
        )
        random_cf_value = 70 if any(
            isinstance(card.card, FinalizationCard) for card in state.discard_pile
        ) else 0
        recovery_value = 80 if any(
            isinstance(card.card, ControlCard) for card in state.discard_pile
        ) else 0
        pressure_goal_penalty = (
            1_000
            if state.pressure + effect.pressure_delta > state.rules.pressure_goal_threshold
            else 0
        )
        return (
            effect.cr_draws * 70
            + effect.draw_main_cards * 55
            + effect.yellow_cards * 30
            + effect.red_cards * 45
            + effect.recover_control_cards * recovery_value
            + effect.play_random_discard_finalizations * random_cf_value
            + pressure_relief * 20
            - max(0, effect.pressure_delta) * 20
            - effect.discard_top_cards * 25
            - effect.player_yellow_cards * 35
            - effect.player_red_cards * 50
            - effect.yellow_injury_rolls * 10
            - effect.red_injury_rolls * 15
            - pressure_goal_penalty
        )
