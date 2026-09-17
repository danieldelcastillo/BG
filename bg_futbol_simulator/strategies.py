"""Estrategias alternativas de IA para escenarios de simulación."""

from __future__ import annotations

from dataclasses import dataclass

from .ai import AutomaticPlayerAI
from .cards import ControlCard, EventCard, EventOption, FinalizationCard
from .engine import IllegalPlay
from .game_state import ControlPlan, ControlPlay, MatchState


@dataclass(frozen=True, slots=True)
class _Candidate:
    """Una secuencia de CC y su resultado previsto para la CF actual."""

    plan: ControlPlan
    extra_player_goals: int
    cr_draws: int
    bot_goal_from_pressure: bool
    final_pressure: int
    tier: int


class OneNilLowCRAI(AutomaticPlayerAI):
    """Estrategia de partido que busca 1–0 y minimiza las CR robadas.

    Hasta la segunda CR conserva las CC para una oportunidad real de gol: solo
    las gasta si con ellas puede marcar. Al llegar a 2 CR, evita nuevas CR antes
    que buscar el gol. Después del primer gol, protege el 1–0: no anota más y
    minimiza CR, presión y gasto de cartas. Al principio también prefiere CE
    que mantengan el mazo o aporten recursos, en lugar de descartar cartas.
    """

    def choose_control_plan(
        self, state: MatchState, finalization: FinalizationCard
    ) -> ControlPlan:
        if state.player_goals >= 1:
            return self._non_scoring_plan(state, finalization)
        if state.cr_draws >= 2:
            return self._cr_first_plan(state, finalization)
        return self._goal_collecting_plan(state, finalization)

    def choose_event_option(self, state: MatchState, event: EventCard) -> EventOption:
        if state.player_goals == 0 and state.cr_draws < 2:
            return min(
                event.options,
                key=lambda option: self._goal_building_event_key(state, option),
            )
        return min(
            event.options,
            key=lambda option: self._event_risk_key(state, option),
        )

    def _goal_collecting_plan(
        self, state: MatchState, finalization: FinalizationCard
    ) -> ControlPlan:
        """Solo gasta CC antes de 2 CR si la secuencia permite marcar."""

        scoring_candidates = [
            candidate
            for candidate in self._candidate_plans(state, finalization)
            if candidate.extra_player_goals > 0
        ]
        if not scoring_candidates:
            return ControlPlan()
        return min(
            scoring_candidates,
            key=lambda candidate: (
                candidate.cr_draws > 0,
                candidate.bot_goal_from_pressure,
                candidate.final_pressure,
                candidate.plan.cards_spent,
                tuple(
                    (play.card_definition_id, play.option_key)
                    for play in candidate.plan.plays
                ),
            ),
        ).plan

    def _cr_first_plan(
        self, state: MatchState, finalization: FinalizationCard
    ) -> ControlPlan:
        """Desde 2 CR, reduce CR incluso si eso aplaza el primer gol."""

        return min(
            self._candidate_plans(state, finalization),
            key=lambda candidate: (
                candidate.cr_draws > 0,
                candidate.bot_goal_from_pressure,
                -candidate.tier,
                candidate.final_pressure,
                candidate.plan.cards_spent,
                tuple(
                    (play.card_definition_id, play.option_key)
                    for play in candidate.plan.plays
                ),
            ),
        ).plan

    def _non_scoring_plan(
        self, state: MatchState, finalization: FinalizationCard
    ) -> ControlPlan:
        """Explora todas las secuencias legales y escoge la mejor para 1–0."""

        return min(self._candidate_plans(state, finalization), key=self._candidate_key).plan

    def _candidate_plans(
        self, state: MatchState, finalization: FinalizationCard
    ) -> list[_Candidate]:
        """Evalúa cada secuencia legal de CC contra la CF pendiente."""

        candidates: list[_Candidate] = []
        frontier: list[tuple[MatchState, ControlPlan]] = [
            (state.clone_for_decision(), ControlPlan())
        ]
        visited: set[tuple[tuple[str, ...], int, int, int]] = set()

        while frontier:
            branch, plan = frontier.pop()
            signature = branch.decision_signature()
            # La misma posición con una secuencia más larga nunca será mejor.
            if signature in visited:
                continue
            visited.add(signature)
            preview = self.engine.evaluate_finalization(branch, finalization)
            candidates.append(
                _Candidate(
                    plan=plan,
                    extra_player_goals=preview.outcome.effect.goals,
                    cr_draws=preview.outcome.effect.cr_draws,
                    bot_goal_from_pressure=preview.projected_bot_goal_from_pressure,
                    final_pressure=preview.projected_pressure,
                    tier=preview.resolution.tier,
                )
            )
            for play in self._legal_plays(branch):
                next_branch = branch.clone_for_decision()
                try:
                    self.engine.apply_control_play(next_branch, play, log=False)
                except IllegalPlay:
                    continue
                frontier.append(
                    (next_branch, ControlPlan((*plan.plays, play)))
                )

        return candidates

    @staticmethod
    def _legal_plays(state: MatchState) -> tuple[ControlPlay, ...]:
        definitions: dict[str, ControlCard] = {}
        for instance in state.hand:
            if isinstance(instance.card, ControlCard):
                definitions.setdefault(instance.card.definition_id, instance.card)
        return tuple(
            ControlPlay(definition_id, option.key)
            for definition_id in sorted(definitions)
            for option in definitions[definition_id].options
        )

    @staticmethod
    def _candidate_key(candidate: _Candidate) -> tuple[object, ...]:
        return (
            candidate.extra_player_goals > 0,
            candidate.cr_draws > 0,
            candidate.bot_goal_from_pressure,
            candidate.final_pressure,
            candidate.plan.cards_spent,
            -candidate.tier,
            tuple((play.card_definition_id, play.option_key) for play in candidate.plan.plays),
        )

    @staticmethod
    def _event_risk_key(state: MatchState, option: EventOption) -> tuple[object, ...]:
        """Ordena CE por riesgo de alejarse del 1–0 sin CR."""

        effect = option.effect
        would_score_bot = state.pressure + effect.pressure_delta > state.rules.pressure_goal_threshold
        return (
            effect.cr_draws > 0,
            effect.draw_main_cards > 0,
            effect.play_random_discard_finalizations > 0,
            would_score_bot,
            effect.player_yellow_cards > 0,
            effect.yellow_injury_rolls > 0 or effect.red_injury_rolls > 0,
            max(0, effect.pressure_delta),
            effect.discard_top_cards,
            option.key,
        )

    @staticmethod
    def _goal_building_event_key(state: MatchState, option: EventOption) -> tuple[object, ...]:
        """Conserva el mazo y busca recursos mientras aún se persigue el 1–0."""

        effect = option.effect
        would_score_bot = state.pressure + effect.pressure_delta > state.rules.pressure_goal_threshold
        return (
            effect.cr_draws > 0,
            would_score_bot,
            effect.player_yellow_cards > 0 or effect.player_red_cards > 0,
            effect.yellow_injury_rolls > 0 or effect.red_injury_rolls > 0,
            effect.discard_top_cards,
            -effect.draw_main_cards,
            -effect.recover_control_cards,
            effect.play_random_discard_finalizations > 0,
            max(0, effect.pressure_delta),
            option.key,
        )
