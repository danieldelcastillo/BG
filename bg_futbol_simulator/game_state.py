"""Estado, resultados y órdenes de juego del simulador."""

from __future__ import annotations

import random
from dataclasses import dataclass, field

from .cards import Attribute, CardInstance, FinalizationCard, OutcomeKind, RedCard


@dataclass(frozen=True, slots=True)
class Team:
    """Atributos permanentes de un equipo."""

    defense: int
    midfield: int
    attack: int

    def __post_init__(self) -> None:
        if min(self.defense, self.midfield, self.attack) < 0:
            raise ValueError("DEF, MED y AT no pueden ser negativos.")

    def value(self, attribute: Attribute) -> int:
        return {
            Attribute.DEF: self.defense,
            Attribute.MED: self.midfield,
            Attribute.AT: self.attack,
        }[attribute]


@dataclass(frozen=True, slots=True)
class MatchRules:
    """Reglas de flujo configurables que no forman parte de una carta."""

    ties_succeed: bool = True
    pressure_floor: int = 0
    pressure_goal_threshold: int = 9
    initial_pressure: int = 0
    max_control_hand_size: int = 5

    def __post_init__(self) -> None:
        if self.pressure_floor < 0:
            raise ValueError("El mínimo de presión no puede ser negativo.")
        if self.pressure_goal_threshold < self.pressure_floor:
            raise ValueError("El umbral de gol por presión no puede estar bajo su mínimo.")
        if not self.pressure_floor <= self.initial_pressure <= self.pressure_goal_threshold:
            raise ValueError("La presión inicial debe estar dentro de sus límites.")
        if self.max_control_hand_size <= 0:
            raise ValueError("El límite de mano de CC debe ser al menos 1.")


@dataclass(frozen=True, slots=True)
class Event:
    """Evento de auditoría legible y serializable de un partido."""

    turn: int
    kind: str
    detail: str


@dataclass(frozen=True, slots=True)
class ControlPlay:
    """Una CC por definición y la única opción que se ha elegido de ella."""

    card_definition_id: str
    option_key: str


@dataclass(frozen=True, slots=True)
class ControlPlan:
    """Secuencia ordenada de CC que se juega inmediatamente antes de una CF."""

    plays: tuple[ControlPlay, ...] = ()

    @property
    def cards_spent(self) -> int:
        return len(self.plays)


@dataclass(frozen=True, slots=True)
class FinalizationResolution:
    """Resultado que se ha seleccionado al resolver una CF."""

    card_name: str
    outcome_name: str
    outcome_kind: OutcomeKind
    tier: int


@dataclass(frozen=True, slots=True)
class EventResolution:
    """Opción elegida al resolver una CE."""

    card_name: str
    option_label: str


@dataclass(frozen=True, slots=True)
class RedCardResolution:
    """Registro detallado de la resolución de una CR para el informe.

    ``applied_action_index`` es 0 o 1 si se aplicó la primera o la segunda
    acción por comparación; ``None`` si ninguna se cumplió y se aplicó el
    efecto de reserva. ``conditional_met`` indica si, de forma independiente,
    también se aplicó el efecto de la esquina inferior izquierda. El resto de
    campos son una fotografía del estado justo tras resolver esta CR.
    """

    card: RedCard
    applied_action_index: int | None
    conditional_met: bool
    player_goals: int
    bot_goals_from_pressure: int
    bot_goals_from_red_cards: int
    pressure: int
    pending_cc_bonus: int
    pending_cf_bonus: int
    cr_draws: int
    hand_size: int
    max_control_hand_size: int
    control_remaining: int
    finalization_remaining: int
    event_remaining: int
    red_available: int


@dataclass(slots=True)
class MatchState:
    """Estado mutable de un único partido.

    La lista ``deck`` usa el final como parte superior para que ``pop()`` sea
    O(1). Las copias de estado se usan exclusivamente por el árbol de decisión.
    """

    player: Team
    opponent: Team
    rules: MatchRules
    deck: list[CardInstance]
    hand: list[CardInstance] = field(default_factory=list)
    discard_pile: list[CardInstance] = field(default_factory=list)
    red_deck: list[CardInstance] = field(default_factory=list)
    red_discard_pile: list[CardInstance] = field(default_factory=list)
    pending_cc_bonus: int = 0
    pending_cf_bonus: int = 0
    pressure: int = 0
    player_goals: int = 0
    bot_goals_from_pressure: int = 0
    bot_goals_from_red_cards: int = 0
    yellow_cards: int = 0
    red_cards: int = 0
    player_yellow_cards: int = 0
    player_red_cards: int = 0
    cr_draws: int = 0
    injury_substitutions: int = 0
    turn: int = 0
    finalizations: list[FinalizationResolution] = field(default_factory=list)
    events_resolved: list[EventResolution] = field(default_factory=list)
    red_card_resolutions: list[RedCardResolution] = field(default_factory=list)
    events: list[Event] = field(default_factory=list)
    randomizer: random.Random = field(default_factory=random.Random, repr=False)

    def __post_init__(self) -> None:
        if self.pressure < self.rules.pressure_floor:
            raise ValueError("La presión está por debajo del mínimo configurado.")

    @property
    def bot_goals(self) -> int:
        """Goles totales del bot: por presión y por gol en contra de una CR."""

        return self.bot_goals_from_pressure + self.bot_goals_from_red_cards

    def clone_for_decision(self) -> "MatchState":
        """Copia mínima para explorar una rama de la CF pendiente.

        El árbol solo optimiza la CF actual. El mazo, los descartes, el
        historial y las CF ya resueltas no participan en sus comparaciones ni
        en su criterio de prioridad; excluirlos evita copiar estructuras cuyo
        tamaño crece durante un millón de simulaciones. Los descartes de una CC
        siguen aplicándose en la ejecución real del motor.
        """

        return MatchState(
            player=self.player,
            opponent=self.opponent,
            rules=self.rules,
            deck=[],
            hand=list(self.hand),
            discard_pile=[],
            pending_cc_bonus=self.pending_cc_bonus,
            pending_cf_bonus=self.pending_cf_bonus,
            pressure=self.pressure,
            player_goals=self.player_goals,
            bot_goals_from_pressure=self.bot_goals_from_pressure,
            bot_goals_from_red_cards=self.bot_goals_from_red_cards,
            yellow_cards=self.yellow_cards,
            red_cards=self.red_cards,
            player_yellow_cards=self.player_yellow_cards,
            player_red_cards=self.player_red_cards,
            cr_draws=self.cr_draws,
            injury_substitutions=self.injury_substitutions,
            turn=self.turn,
            randomizer=self.randomizer,
        )

    def decision_signature(self) -> tuple[tuple[str, ...], int, int, int]:
        """Estado relevante para una decisión local antes de una CF.

        El orden e identidad de copias idénticas no cambia ninguna transición de
        la CC actual, por lo que se normaliza. El mazo no entra: descartarlo no
        altera la CF pendiente ni las comparaciones de CC.
        """

        return (
            tuple(sorted(instance.card.definition_id for instance in self.hand)),
            self.pending_cc_bonus,
            self.pending_cf_bonus,
            self.pressure,
        )


@dataclass(frozen=True, slots=True)
class MatchResult:
    """Resumen inmutable producido al agotar el mazo."""

    player_goals: int
    bot_goals_from_pressure: int
    bot_goals_from_red_cards: int
    yellow_cards: int
    red_cards: int
    player_yellow_cards: int
    player_red_cards: int
    cr_draws: int
    injury_substitutions: int
    final_pressure: int
    control_cards_left: int
    finalizations: tuple[FinalizationResolution, ...]
    events_resolved: tuple[EventResolution, ...]

    @property
    def finalization_count(self) -> int:
        return len(self.finalizations)

    @property
    def bot_goals(self) -> int:
        """Goles del bot: por presión y por gol en contra de una CR."""

        return self.bot_goals_from_pressure + self.bot_goals_from_red_cards


def result_from_state(state: MatchState) -> MatchResult:
    return MatchResult(
        player_goals=state.player_goals,
        bot_goals_from_pressure=state.bot_goals_from_pressure,
        bot_goals_from_red_cards=state.bot_goals_from_red_cards,
        yellow_cards=state.yellow_cards,
        red_cards=state.red_cards,
        player_yellow_cards=state.player_yellow_cards,
        player_red_cards=state.player_red_cards,
        cr_draws=state.cr_draws,
        injury_substitutions=state.injury_substitutions,
        final_pressure=state.pressure,
        control_cards_left=len(state.hand),
        finalizations=tuple(state.finalizations),
        events_resolved=tuple(state.events_resolved),
    )


def require_finalization(card: CardInstance) -> FinalizationCard:
    """Ayuda de tipado para puntos del motor que reciben una CF."""

    if not isinstance(card.card, FinalizationCard):
        raise TypeError(f"{card.card.name} no es una carta de finalización.")
    return card.card
