"""Motor determinista que aplica las reglas del sistema de partido."""

from __future__ import annotations

import random
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING

from .cards import (
    CardInstance,
    Comparison,
    ControlCard,
    Effect,
    EventCard,
    FinalizationCard,
    FinalizationOutcome,
    RedCard,
    RedComparison,
    RivalCondition,
    build_match_deck,
    build_red_card_deck,
    strong_team_handicap_card,
    weak_team_support_card,
)
from .game_state import (
    ControlPlan,
    ControlPlay,
    Event,
    EventResolution,
    FinalizationResolution,
    MatchResult,
    MatchRules,
    MatchState,
    RedCardResolution,
    Team,
    generate_players,
    result_from_state,
)

if TYPE_CHECKING:
    from .ai import AutomaticPlayerAI


class IllegalPlay(ValueError):
    """La IA o un cliente intentó ejecutar una jugada que no es legal."""


@dataclass(frozen=True, slots=True)
class FinalizationPreview:
    """Resultado de evaluar una CF sin mutar el estado."""

    outcome: FinalizationOutcome
    resolution: FinalizationResolution
    projected_pressure: int
    projected_bot_goal_from_pressure: bool


class RulesEngine:
    """Único punto que puede mutar un :class:`MatchState`.

    El árbol de decisión usa los mismos métodos de este motor sobre copias de
    estado. Así, una jugada explorada y la misma jugada ejecutada obedecen a
    reglas idénticas.
    """

    def create_match_state(
        self,
        player: Team,
        opponent: Team,
        rng: random.Random,
        rules: MatchRules | None = None,
    ) -> MatchState:
        """Crea y baraja el mazo definitivo para un partido."""

        active_rules = rules or MatchRules()
        player = self._with_players(player, rng)
        deck = build_match_deck()
        deck.extend(self._balance_cards(player, opponent))
        rng.shuffle(deck)
        red_deck = build_red_card_deck()
        rng.shuffle(red_deck)
        return MatchState(
            player=player,
            opponent=opponent,
            rules=active_rules,
            deck=deck,
            red_deck=red_deck,
            pressure=active_rules.initial_pressure,
            randomizer=rng,
        )

    @staticmethod
    def _with_players(team: Team, rng: random.Random) -> Team:
        """Genera la plantilla de 7 jugadores del equipo si aún no la tiene.

        El bot no usa plantilla: sus tarjetas se resuelven con la mecánica de
        dado propia, no expulsando jugadores concretos.
        """

        if team.players:
            return team
        return replace(team, players=generate_players(team.defense, team.midfield, team.attack, rng))

    @staticmethod
    def _balance_cards(player: Team, opponent: Team) -> list[CardInstance]:
        """Añade cartas de equilibrio según la diferencia total de atributos.

        Por cada 10 puntos que el jugador quede por debajo del rival (suma de
        DEF+MED+AT) se añade una copia de "La fuerza del débil"; por cada 10
        puntos que quede por encima, una copia de "La fuerza del rival Débil".
        """

        player_total = player.defense + player.midfield + player.attack
        opponent_total = opponent.defense + opponent.midfield + opponent.attack
        gap = opponent_total - player_total
        instances: list[CardInstance] = []
        if gap >= 10:
            card = weak_team_support_card()
            for copy_number in range(1, gap // 10 + 1):
                instances.append(CardInstance(f"{card.definition_id}-{copy_number}", card))
        elif gap <= -10:
            card = strong_team_handicap_card()
            for copy_number in range(1, (-gap) // 10 + 1):
                instances.append(CardInstance(f"{card.definition_id}-{copy_number}", card))
        return instances

    def comparison_succeeds(
        self,
        state: MatchState,
        comparison: Comparison,
        temporary_bonus: int = 0,
    ) -> bool:
        """Resuelve una comparación aplicando el bono temporal al jugador."""

        return self.comparison_succeeds_for_teams(
            state.player,
            state.opponent,
            state.rules,
            comparison,
            temporary_bonus,
        )

    @staticmethod
    def comparison_succeeds_for_teams(
        player: Team,
        opponent: Team,
        rules: MatchRules,
        comparison: Comparison,
        temporary_bonus: int = 0,
    ) -> bool:
        """Versión pura de una comparación, reutilizable por el árbol de IA."""

        player_value = player.value(comparison.player_attribute) + temporary_bonus
        opponent_value = opponent.value(comparison.opponent_attribute) + comparison.opponent_modifier
        ties_succeed = (
            rules.ties_succeed
            if comparison.ties_succeed is None
            else comparison.ties_succeed
        )
        return player_value >= opponent_value if ties_succeed else player_value > opponent_value

    def draw_next_card(self, state: MatchState, *, log: bool = True) -> CardInstance | None:
        """Roba la siguiente carta del mazo.

        Una CC entra automáticamente en la mano. Una CF se devuelve al llamador
        para permitir la decisión de IA antes de resolverla.
        """

        if not state.deck:
            return None
        instance = state.deck.pop()
        state.turn += 1
        if isinstance(instance.card, ControlCard):
            state.hand.append(instance)
            if log:
                self._log(state, "robo_cc", f"Roba CC: {instance.card.name}")
        elif isinstance(instance.card, FinalizationCard):
            if log:
                self._log(state, "robo_cf", f"Aparece CF: {instance.card.name}")
        else:
            if log:
                self._log(state, "robo_ce", f"Aparece CE: {instance.card.name}")
        return instance

    def discard_top_cards(
        self, state: MatchState, count: int, *, log: bool = True
    ) -> tuple[CardInstance, ...]:
        """Descarta hasta ``count`` cartas de la parte superior sin resolverlas."""

        if count < 0:
            raise ValueError("No se puede descartar una cantidad negativa de cartas.")
        discarded: list[CardInstance] = []
        for _ in range(min(count, len(state.deck))):
            discarded.append(state.deck.pop())
        state.discard_pile.extend(discarded)
        if discarded and log:
            names = ", ".join(card.card.name for card in discarded)
            self._log(state, "descarte_mazo", f"Descarta del mazo: {names}")
        return tuple(discarded)

    def apply_control_play(
        self, state: MatchState, play: ControlPlay, *, log: bool = True
    ) -> None:
        """Aplica una CC y exactamente una de sus tres opciones.

        El bono ``+CC`` pendiente se consume al jugar la carta, incluso al optar
        por el efecto base. Si la propia opción concede ``+CC``, pasa a ser el
        nuevo bono para la siguiente CC.
        """

        hand_index, instance = self._find_control_card(state, play.card_definition_id)
        card = instance.card
        assert isinstance(card, ControlCard)
        option = card.option(play.option_key)

        current_cc_bonus = state.pending_cc_bonus
        state.pending_cc_bonus = 0
        if option.comparison is not None and not self.comparison_succeeds(
            state, option.comparison, current_cc_bonus
        ):
            state.pending_cc_bonus = current_cc_bonus
            raise IllegalPlay(
                f"No se supera {option.label} de {card.name} con el bono +CC actual."
            )

        state.hand.pop(hand_index)
        state.discard_pile.append(instance)
        self.apply_effect(state, option.effect, log=log)
        if log:
            self._log(state, "juega_cc", f"Juega {card.name}: {option.label}")

    def execute_control_plan(
        self, state: MatchState, plan: ControlPlan, *, log: bool = True
    ) -> None:
        """Ejecuta la secuencia ordenada de CC elegida por la IA."""

        for play in plan.plays:
            self.apply_control_play(state, play, log=log)

    def discard_control_from_hand(
        self, state: MatchState, definition_id: str, *, log: bool = True
    ) -> CardInstance:
        """Descarta una CC de la mano por límite o efecto de una carta."""

        index, instance = self._find_control_card(state, definition_id)
        state.hand.pop(index)
        state.discard_pile.append(instance)
        if log:
            self._log(state, "descarte_mano_cc", f"Descarta de la mano: {instance.card.name}")
        return instance

    def evaluate_finalization(
        self, state: MatchState, card: FinalizationCard
    ) -> FinalizationPreview:
        """Selecciona el primer resultado de CF cuya comparación se supera."""

        return self.evaluate_finalization_for_values(
            state.player,
            state.opponent,
            state.rules,
            state.pending_cf_bonus,
            state.pressure,
            card,
        )

    def evaluate_finalization_for_values(
        self,
        player: Team,
        opponent: Team,
        rules: MatchRules,
        pending_cf_bonus: int,
        pressure: int,
        card: FinalizationCard,
    ) -> FinalizationPreview:
        """Versión pura de la CF para la búsqueda de decisiones."""

        for outcome in card.outcomes:
            if outcome.comparison is None or self.comparison_succeeds_for_teams(
                player, opponent, rules, outcome.comparison, pending_cf_bonus
            ):
                resolution = FinalizationResolution(
                    card_name=card.name,
                    outcome_name=outcome.name,
                    outcome_kind=outcome.kind,
                    tier=outcome.tier,
                )
                projected_pressure, bot_goal_from_pressure = self.pressure_after_delta(
                    rules, pressure, outcome.effect.pressure_delta
                )
                return FinalizationPreview(
                    outcome,
                    resolution,
                    projected_pressure,
                    bot_goal_from_pressure,
                )
        raise RuntimeError(f"La CF {card.name} no tiene un resultado de reserva.")

    def resolve_finalization(
        self,
        state: MatchState,
        instance: CardInstance,
        ai: "AutomaticPlayerAI | None" = None,
        *,
        log: bool = True,
        return_to_discard: bool = True,
    ) -> FinalizationResolution:
        """Consume el +CF actual, ejecuta primero el condicional y después la CF."""

        if not isinstance(instance.card, FinalizationCard):
            raise TypeError(f"{instance.card.name} no es una carta de finalización.")
        # El +CF que ya estaba pendiente pertenece a esta CF. Lo guardamos
        # y lo consumimos antes de ejecutar el condicional para que cualquier
        # +CF generado por el condicional quede disponible para una CF futura.
        current_cf_bonus = state.pending_cf_bonus
        state.pending_cf_bonus = 0

        # El condicional de una CF se comprueba y ejecuta ANTES del resultado
        # principal de la carta.
        conditional = instance.card.conditional
        conditional_met = (
            conditional is not None
            and self._rival_condition_met(state, conditional.condition)
        )
        if conditional_met:
            assert conditional is not None
            if log:
                self._log(state, "cf_condicional", conditional.label)
            self._apply_full_effect(state, conditional.effect, ai, log=log)

        # El resultado principal se determina después del condicional, usando
        # exclusivamente el +CF que pertenecía a esta CF.
        preview = self.evaluate_finalization_for_values(
            state.player,
            state.opponent,
            state.rules,
            current_cf_bonus,
            state.pressure,
            instance.card,
        )
        self._apply_full_effect(state, preview.outcome.effect, ai, log=log)

        if return_to_discard:
            state.discard_pile.append(instance)

        resolution = FinalizationResolution(
            card_name=preview.resolution.card_name,
            outcome_name=preview.resolution.outcome_name,
            outcome_kind=preview.resolution.outcome_kind,
            tier=preview.resolution.tier,
            conditional_met=conditional_met,
        )
        state.finalizations.append(resolution)
        if log:
            self._log(
                state,
                "resuelve_cf",
                f"{instance.card.name}: {resolution.outcome_name}",
            )
        return resolution

    def resolve_event(
        self, state: MatchState, instance: CardInstance, ai: "AutomaticPlayerAI", *, log: bool = True
    ) -> EventResolution:
        """Resuelve una CE y sus efectos sobre el mazo, mano o descarte."""

        if not isinstance(instance.card, EventCard):
            raise TypeError(f"{instance.card.name} no es una carta de evento.")
        option = ai.choose_event_option(state, instance.card)
        self._apply_full_effect(state, option.effect, ai, log=log)
        resolution = EventResolution(instance.card.name, option.label)
        state.events_resolved.append(resolution)
        state.discard_pile.append(instance)
        if log:
            self._log(state, "resuelve_ce", f"{instance.card.name}: {option.label}")
        return resolution

    def resolve_red_card(
        self,
        state: MatchState,
        instance: CardInstance,
        ai: "AutomaticPlayerAI | None" = None,
        *,
        log: bool = True,
    ) -> None:
        """Resuelve una CR aplicando una única acción obligatoria más una acción
        independiente condicionada al marcador.

        Primero se comprueba y aplica, de forma independiente, la condición
        de marcador de la esquina inferior izquierda. Después se recorre la
        carta de arriba hacia abajo: se aplica la primera de las dos acciones
        cuya comparación se cumpla o, si ninguna se cumple, el efecto de
        reserva (esquina inferior derecha, sin condición).
        """

        card = instance.card
        assert isinstance(card, RedCard)
        effective_ai = self._resolve_ai(ai)

        # El condicional de la CR se comprueba y ejecuta ANTES de resolver
        # cualquiera de las acciones principales de la carta.
        conditional_met = self._rival_condition_met(state, card.conditional.condition)
        if conditional_met:
            if log:
                self._log(state, "cr_condicion", card.conditional.label)
            self._apply_full_effect(state, card.conditional.effect, effective_ai, log=log)

        applied_action_index = None
        chosen_action = None
        for index, action in enumerate(card.actions):
            if self.red_comparison_succeeds(state, action.comparison):
                chosen_action = action
                applied_action_index = index
                break
        if chosen_action is not None:
            self._apply_full_effect(state, chosen_action.effect, effective_ai, log=log)
            if log:
                self._log(state, "cr_accion", f"{card.name}: {chosen_action.label}")
        else:
            self._apply_full_effect(state, card.fallback_effect, effective_ai, log=log)
            if log:
                self._log(state, "cr_accion", f"{card.name}: acción de reserva")

        state.red_discard_pile.append(instance)
        state.red_card_resolutions.append(
            RedCardResolution(
                card=card,
                applied_action_index=applied_action_index,
                conditional_met=conditional_met,
                player_goals=state.player_goals,
                bot_goals_from_pressure=state.bot_goals_from_pressure,
                bot_goals_from_red_cards=state.bot_goals_from_red_cards,
                pressure=state.pressure,
                pending_cc_bonus=state.pending_cc_bonus,
                pending_cf_bonus=state.pending_cf_bonus,
                cr_draws=state.cr_draws,
                hand_size=len(state.hand),
                max_control_hand_size=state.rules.max_control_hand_size,
                control_remaining=sum(isinstance(i.card, ControlCard) for i in state.deck),
                finalization_remaining=sum(
                    isinstance(i.card, FinalizationCard) for i in state.deck
                ),
                event_remaining=sum(isinstance(i.card, EventCard) for i in state.deck),
                red_available=len(state.red_deck) + len(state.red_discard_pile),
            )
        )

    @staticmethod
    def red_comparison_succeeds(state: MatchState, comparison: RedComparison) -> bool:
        """Compara el atributo rival contra el propio (más el margen)."""

        rival_value = state.opponent.value(comparison.rival_attribute)
        player_value = state.player.value(comparison.player_attribute) + comparison.player_modifier
        if comparison.rival_must_be_lower:
            return rival_value < player_value
        return rival_value > player_value

    def draw_red_card(self, state: MatchState, *, log: bool = True) -> CardInstance | None:
        """Roba la siguiente CR, reciclando su descarte si el mazo está vacío."""

        if not state.red_deck:
            if not state.red_discard_pile:
                return None
            state.red_deck, state.red_discard_pile = state.red_discard_pile, []
            state.randomizer.shuffle(state.red_deck)
            if log:
                self._log(state, "reciclaje_cr", "Se baraja el descarte de CR para formar un nuevo mazo")
        instance = state.red_deck.pop()
        if log:
            self._log(state, "roba_cr", f"Roba CR: {instance.card.name}")
        return instance

    @staticmethod
    def _rival_condition_met(state: MatchState, condition: RivalCondition) -> bool:
        bot_goals = state.bot_goals_from_pressure + state.bot_goals_from_red_cards
        if condition is RivalCondition.RIVAL_WINNING:
            return bot_goals > state.player_goals
        return bot_goals < state.player_goals

    def _resolve_ai(self, ai: "AutomaticPlayerAI | None") -> "AutomaticPlayerAI":
        if ai is not None:
            return ai
        from .ai import AutomaticPlayerAI

        return AutomaticPlayerAI(self)

    def _draw_and_resolve_red_card(
        self, state: MatchState, ai: "AutomaticPlayerAI", *, log: bool
    ) -> None:
        drawn = self.draw_red_card(state, log=log)
        if drawn is not None:
            self.resolve_red_card(state, drawn, ai, log=log)

    def apply_effect(self, state: MatchState, effect: Effect, *, log: bool = True) -> None:
        """Aplica los componentes puramente aditivos de un efecto.

        Los componentes que dependen de una decisión de IA (descartar,
        recuperar, robar cartas...) se aplican en :meth:`_apply_dependent_effects`.
        """

        state.pending_cc_bonus += effect.cc_bonus
        state.pending_cf_bonus += effect.cf_bonus
        state.pressure, bot_goal = self.pressure_after_delta(
            state.rules, state.pressure, effect.pressure_delta
        )
        if bot_goal:
            state.bot_goals_from_pressure += 1
            if log:
                self._log(state, "gol_bot_presion", "El bot marca por superar presión 9; presión a 0")
        state.player_goals += effect.goals
        state.bot_goals_from_red_cards += effect.bot_goals
        if effect.bot_goals and log:
            self._log(state, "gol_en_contra", "Gol en contra por una CR")
        for _ in range(effect.yellow_cards):
            self._bot_yellow_card(state, log=log)
        for _ in range(effect.red_cards):
            state.red_cards += 1
            self._apply_bot_red_card_penalty(state, log=log)
        for _ in range(effect.player_yellow_cards):
            state.player_yellow_cards += 1
            if self._card_random_player(state, state.player, "tu equipo", log=log):
                state.player_red_cards += 1
        for _ in range(effect.player_red_cards):
            state.player_red_cards += 1
            self._send_off_random_player(state, state.player, "tu equipo", log=log)
        self._roll_injuries(state, effect.yellow_injury_rolls, 0.10, "amarilla", log=log)
        self._roll_injuries(state, effect.red_injury_rolls, 0.15, "roja", log=log)
        if effect.discard_top_cards:
            self.discard_top_cards(state, effect.discard_top_cards, log=log)

    def _bot_yellow_card(self, state: MatchState, *, log: bool) -> None:
        """El bot no tiene plantilla: cada amarilla tira un d8 y lo suma al
        total de amarillas del partido; si supera 10, se convierte en roja y
        se retiran dos amarillas acumuladas.
        """

        state.yellow_cards += 1
        roll = state.randomizer.randint(1, 8)
        total = roll + state.yellow_cards
        if log:
            self._log(
                state,
                "amarilla_bot",
                f"Amarilla al bot: tirada d8={roll} + {state.yellow_cards} amarillas = {total}",
            )
        if total > 10:
            state.yellow_cards = max(0, state.yellow_cards - 2)
            state.red_cards += 1
            self._apply_bot_red_card_penalty(state, log=log)

    def _apply_bot_red_card_penalty(self, state: MatchState, *, log: bool) -> None:
        """El bot pierde 2 MED y 4 AT de forma permanente por cada roja."""

        opponent = state.opponent
        state.opponent = replace(
            opponent,
            midfield=max(0, opponent.midfield - 2),
            attack=max(0, opponent.attack - 4),
        )
        if log:
            self._log(state, "expulsion", "El bot recibe una roja: -2 MED y -4 AT")

    def _send_off_random_player(
        self, state: MatchState, team: Team, label: str, *, log: bool
    ) -> None:
        """Expulsa a un jugador activo al azar; deja de sumar al equipo."""

        active = [player for player in team.players if not player.sent_off]
        if not active:
            return
        player = state.randomizer.choice(active)
        player.sent_off = True
        if log:
            self._log(
                state,
                "expulsion",
                f"Roja directa: expulsado un jugador de {label} "
                f"({player.attribute.value} {player.value})",
            )

    def _card_random_player(
        self, state: MatchState, team: Team, label: str, *, log: bool
    ) -> bool:
        """Amonesta a un jugador activo al azar.

        Devuelve ``True`` si era su segunda amarilla y, por tanto, queda
        expulsado (roja por acumulación).
        """

        active = [player for player in team.players if not player.sent_off]
        if not active:
            return False
        player = state.randomizer.choice(active)
        player.yellow_cards += 1
        if log:
            self._log(
                state,
                "amarilla_jugador",
                f"Amarilla para un jugador de {label} "
                f"({player.attribute.value} {player.value}); acumula {player.yellow_cards}",
            )
        if player.yellow_cards >= 2:
            player.sent_off = True
            if log:
                self._log(
                    state,
                    "expulsion",
                    f"Segunda amarilla: expulsado un jugador de {label} "
                    f"({player.attribute.value} {player.value})",
                )
            return True
        return False

    def _apply_dependent_effects(
        self, state: MatchState, effect: Effect, ai: "AutomaticPlayerAI", *, log: bool = True
    ) -> None:
        """Aplica los componentes de un efecto que requieren una decisión de IA."""

        for _ in range(effect.discard_control_cards):
            if not state.hand:
                if log:
                    self._log(state, "descarte_mano_cc", "No hay CC en mano para descartar")
                break
            self.discard_control_from_hand(state, ai.choose_control_discard(state), log=log)
        for _ in range(effect.recover_control_cards):
            self._recover_control_from_discard(state, ai, log=log)
        for _ in range(effect.play_random_discard_finalizations):
            self._play_random_discard_finalization(state, ai, log=log)
        for _ in range(effect.draw_main_cards):
            drawn = self.draw_next_card(state, log=log)
            if drawn is not None:
                self._resolve_drawn_card(state, drawn, ai)
        for _ in range(effect.cr_draws):
            state.cr_draws += 1
            self._draw_and_resolve_red_card(state, ai, log=log)
        for _ in range(effect.draw_red_cards):
            self._draw_and_resolve_red_card(state, ai, log=log)

    def _apply_full_effect(
        self,
        state: MatchState,
        effect: Effect,
        ai: "AutomaticPlayerAI | None",
        *,
        log: bool = True,
    ) -> None:
        """Aplica un efecto completo: componentes aditivos y dependientes de IA."""

        self.apply_effect(state, effect, log=log)
        self._apply_dependent_effects(state, effect, self._resolve_ai(ai), log=log)

    @staticmethod
    def pressure_after_delta(
        rules: MatchRules, pressure: int, delta: int
    ) -> tuple[int, bool]:
        """Aplica presión y devuelve si el bot marca al superar el umbral."""

        updated = max(rules.pressure_floor, pressure + delta)
        if updated > rules.pressure_goal_threshold:
            return rules.pressure_floor, True
        return updated, False

    def play_match(self, state: MatchState, ai: "AutomaticPlayerAI") -> MatchResult:
        """Ejecuta un partido hasta que el mazo queda vacío."""

        while (instance := self.draw_next_card(state)) is not None:
            self._resolve_drawn_card(state, instance, ai)
        return result_from_state(state)

    def _resolve_drawn_card(
        self, state: MatchState, instance: CardInstance, ai: "AutomaticPlayerAI"
    ) -> None:
        """Aplica el flujo normal de una carta, también tras un robo de CE."""

        if isinstance(instance.card, ControlCard):
            while len(state.hand) > state.rules.max_control_hand_size:
                self.discard_control_from_hand(state, ai.choose_control_discard(state))
            return
        if isinstance(instance.card, FinalizationCard):
            plan = ai.choose_control_plan(state, instance.card)
            self.execute_control_plan(state, plan)
            self.resolve_finalization(state, instance, ai)
            return
        self.resolve_event(state, instance, ai)

    def _recover_control_from_discard(
        self, state: MatchState, ai: "AutomaticPlayerAI", *, log: bool
    ) -> None:
        candidates = [card for card in state.discard_pile if isinstance(card.card, ControlCard)]
        if not candidates:
            return
        definition_id = ai.choose_control_recovery(state, tuple(candidates))
        index = next(
            index
            for index, candidate in enumerate(state.discard_pile)
            if candidate.card.definition_id == definition_id
        )
        recovered = state.discard_pile.pop(index)
        state.hand.append(recovered)
        if log:
            self._log(state, "recupera_cc", f"Recupera del descarte: {recovered.card.name}")
        while len(state.hand) > state.rules.max_control_hand_size:
            self.discard_control_from_hand(state, ai.choose_control_discard(state), log=log)

    def _play_random_discard_finalization(
        self, state: MatchState, ai: "AutomaticPlayerAI", *, log: bool
    ) -> None:
        candidates = [card for card in state.discard_pile if isinstance(card.card, FinalizationCard)]
        if not candidates:
            return
        finalization = state.randomizer.choice(candidates)
        if log:
            self._log(state, "cf_aleatoria_descarte", f"Juega CF aleatoria: {finalization.card.name}")
        # "Inmediatamente" impide jugar CC antes de esta CF extra.
        self.resolve_finalization(state, finalization, ai, log=log, return_to_discard=False)

    def _roll_injuries(
        self,
        state: MatchState,
        rolls: int,
        probability: float,
        source: str,
        *,
        log: bool,
    ) -> None:
        for _ in range(rolls):
            if state.randomizer.random() < probability:
                state.injury_substitutions += 1
                position = state.randomizer.choice(("DEF", "MED", "AT"))
                if log:
                    self._log(state, "lesion", f"Lesión por {source}: sustitución aleatoria ({position})")

    @staticmethod
    def _find_control_card(
        state: MatchState, definition_id: str
    ) -> tuple[int, CardInstance]:
        for index, instance in enumerate(state.hand):
            if instance.card.definition_id == definition_id:
                if not isinstance(instance.card, ControlCard):
                    break
                return index, instance
        raise IllegalPlay(f"No hay una CC {definition_id!r} en la mano.")

    @staticmethod
    def _log(state: MatchState, kind: str, detail: str) -> None:
        state.events.append(Event(state.turn, kind, detail))
