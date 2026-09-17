"""Búsqueda exacta de las secuencias de CC antes de una CF."""

from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass

from .cards import ControlCard, FinalizationCard, card_catalogue
from .engine import RulesEngine
from .game_state import ControlPlan, ControlPlay, MatchState


@dataclass(frozen=True, slots=True)
class SearchDiagnostics:
    """Información para medir el coste de una decisión de IA."""

    expanded_states: int
    cache_hits: int


@dataclass(frozen=True, slots=True)
class _DecisionPosition:
    """Parte del estado que puede cambiar antes de resolver la CF actual."""

    hand: tuple[str, ...]
    pending_cc_bonus: int
    pending_cf_bonus: int
    pressure: int


@dataclass(frozen=True, slots=True)
class _SearchResult:
    """Mejor resultado alcanzable desde una posición de decisión."""

    plan: ControlPlan
    tier: int
    projected_pressure: int
    projected_bot_goal_from_pressure: bool

    @property
    def canonical_plan(self) -> tuple[tuple[str, str], ...]:
        return DecisionTree._plan_key(self.plan)


@dataclass(frozen=True, slots=True)
class _SearchNode:
    """Posición y secuencia que la ha alcanzado en una profundidad concreta."""

    position: _DecisionPosition
    plan: ControlPlan


class DecisionTree:
    """Explora todas las jugadas legales mediante búsqueda por capas exacta.

    La búsqueda usa una representación mínima y pura de las variables que
    pueden afectar la CF pendiente: mano, +CC, +CF y presión. El motor comparte
    sus funciones puras de comparación y CF, por lo que esta optimización no
    duplica ni altera reglas. El mazo, el descarte y el historial no afectan a
    ninguna comparación antes de esa CF y se aplican normalmente al ejecutar la
    jugada ganadora en :mod:`engine`.
    """

    def __init__(self, engine: RulesEngine, *, cache_limit: int = 250_000) -> None:
        if cache_limit <= 0:
            raise ValueError("cache_limit debe ser mayor que cero.")
        self.engine = engine
        self.cache_limit = cache_limit
        self._control_cards = {
            card.definition_id: card
            for card in card_catalogue().values()
            if isinstance(card, ControlCard)
        }
        self._policy_cache: OrderedDict[tuple[object, ...], _SearchResult] = OrderedDict()
        self.last_diagnostics = SearchDiagnostics(0, 0)

    def choose_plan(self, state: MatchState, finalization: FinalizationCard) -> ControlPlan:
        """Devuelve la secuencia que maximiza el resultado de la CF.

        Criterios, en orden: resultado de la CF, menor número de CC gastadas,
        menor presión final y orden canónico estable. La búsqueda se detiene en
        la primera capa con resultado superior: una capa posterior no puede
        mejorar su tier y gastaría más CC, por lo que la cota es exacta.
        """

        initial = _DecisionPosition(
            hand=tuple(sorted(instance.card.definition_id for instance in state.hand)),
            pending_cc_bonus=state.pending_cc_bonus,
            pending_cf_bonus=state.pending_cf_bonus,
            pressure=state.pressure,
        )
        key = self._cache_key(state, finalization, initial)
        cached = self._policy_cache.get(key)
        if cached is not None:
            self._policy_cache.move_to_end(key)
            self.last_diagnostics = SearchDiagnostics(0, 1)
            return cached.plan

        expanded_states = 1
        baseline = self._evaluate(state, initial, finalization)
        baseline_result = _SearchResult(
            plan=ControlPlan(),
            tier=baseline.resolution.tier,
            projected_pressure=baseline.projected_pressure,
            projected_bot_goal_from_pressure=baseline.projected_bot_goal_from_pressure,
        )
        if baseline_result.tier == 2:
            self._store(key, baseline_result)
            self.last_diagnostics = SearchDiagnostics(expanded_states, 0)
            return baseline_result.plan

        # Si no hay un resultado medio inmediato, guardamos el primero que se
        # encuentre. Seguimos explorando para demostrar si existe uno superior.
        best_middle = baseline_result if baseline_result.tier == 1 else None
        frontier: dict[_DecisionPosition, _SearchNode] = {
            initial: _SearchNode(initial, ControlPlan())
        }

        for _depth in range(1, len(initial.hand) + 1):
            next_frontier: dict[_DecisionPosition, _SearchNode] = {}
            for node in sorted(frontier.values(), key=lambda item: self._plan_key(item.plan)):
                for play in self._legal_next_plays(node.position):
                    position = self._apply_play(state, node.position, play)
                    if position is None:
                        continue
                    candidate = _SearchNode(
                        position, ControlPlan((*node.plan.plays, play))
                    )
                    existing = next_frontier.get(position)
                    if existing is None or self._prefer_node(candidate, existing):
                        next_frontier[position] = candidate

            if not next_frontier:
                break
            expanded_states += len(next_frontier)

            high_candidates: list[_SearchResult] = []
            middle_candidates: list[_SearchResult] = []
            for node in next_frontier.values():
                preview = self._evaluate(state, node.position, finalization)
                result = _SearchResult(
                    plan=node.plan,
                    tier=preview.resolution.tier,
                    projected_pressure=preview.projected_pressure,
                    projected_bot_goal_from_pressure=preview.projected_bot_goal_from_pressure,
                )
                if result.tier == 2:
                    high_candidates.append(result)
                elif result.tier == 1 and best_middle is None:
                    middle_candidates.append(result)

            if high_candidates:
                best = self._best(high_candidates)
                self._store(key, best)
                self.last_diagnostics = SearchDiagnostics(expanded_states, 0)
                return best.plan

            if middle_candidates:
                best_middle = self._best(middle_candidates)
            frontier = next_frontier

        # Si no se encontró un resultado superior, se prioriza el resultado
        # medio que costó menos CC. Si tampoco existe, no se gasta ninguna.
        result = best_middle or baseline_result
        self._store(key, result)
        self.last_diagnostics = SearchDiagnostics(expanded_states, 0)
        return result.plan

    def clear_cache(self) -> None:
        """Libera las políticas memorizadas; útil en experimentos aislados."""

        self._policy_cache.clear()

    def _evaluate(
        self,
        state: MatchState,
        position: _DecisionPosition,
        finalization: FinalizationCard,
    ):
        return self.engine.evaluate_finalization_for_values(
            state.player,
            state.opponent,
            state.rules,
            position.pending_cf_bonus,
            position.pressure,
            finalization,
        )

    def _apply_play(
        self,
        state: MatchState,
        position: _DecisionPosition,
        play: ControlPlay,
    ) -> _DecisionPosition | None:
        """Transición pura equivalente a jugar una CC en el motor."""

        card = self._control_cards[play.card_definition_id]
        option = card.option(play.option_key)
        if option.comparison is not None and not self.engine.comparison_succeeds_for_teams(
            state.player,
            state.opponent,
            state.rules,
            option.comparison,
            position.pending_cc_bonus,
        ):
            return None

        hand = list(position.hand)
        hand.remove(play.card_definition_id)
        effect = option.effect
        return _DecisionPosition(
            hand=tuple(hand),
            # +CC vigente se consume al jugar esta carta. Solo el +CC que
            # produzca la opción elegida puede llegar a la siguiente CC.
            pending_cc_bonus=effect.cc_bonus,
            pending_cf_bonus=position.pending_cf_bonus + effect.cf_bonus,
            pressure=self.engine.pressure_after_delta(
                state.rules, position.pressure, effect.pressure_delta
            )[0],
        )

    def _legal_next_plays(self, position: _DecisionPosition) -> tuple[ControlPlay, ...]:
        plays: list[ControlPlay] = []
        for definition_id in dict.fromkeys(position.hand):
            card = self._control_cards[definition_id]
            for option in card.options:
                plays.append(ControlPlay(definition_id, option.key))
        return tuple(plays)

    @staticmethod
    def _prefer_node(candidate: _SearchNode, incumbent: _SearchNode) -> bool:
        """Elige una representación estable para una misma posición exacta."""

        return DecisionTree._plan_key(candidate.plan) < DecisionTree._plan_key(incumbent.plan)

    @staticmethod
    def _plan_key(plan: ControlPlan) -> tuple[tuple[str, str], ...]:
        return tuple((play.card_definition_id, play.option_key) for play in plan.plays)

    @staticmethod
    def _best(candidates: list[_SearchResult]) -> _SearchResult:
        return min(
            candidates,
            key=lambda result: (
                result.plan.cards_spent,
                result.projected_bot_goal_from_pressure,
                result.projected_pressure,
                result.canonical_plan,
            ),
        )

    @staticmethod
    def _cache_key(
        state: MatchState,
        finalization: FinalizationCard,
        position: _DecisionPosition,
    ) -> tuple[object, ...]:
        """Clave de estado suficiente para una única CF pendiente."""

        return (
            finalization.definition_id,
            state.player.defense,
            state.player.midfield,
            state.player.attack,
            state.opponent.defense,
            state.opponent.midfield,
            state.opponent.attack,
            state.rules.ties_succeed,
            state.rules.pressure_floor,
            state.rules.pressure_goal_threshold,
            position,
        )

    def _store(self, key: tuple[object, ...], result: _SearchResult) -> None:
        self._policy_cache[key] = result
        self._policy_cache.move_to_end(key)
        if len(self._policy_cache) > self.cache_limit:
            self._policy_cache.popitem(last=False)
