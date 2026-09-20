"""Estado, resultados y órdenes de juego del simulador."""

from __future__ import annotations

import random
from dataclasses import dataclass, field, replace

from .cards import Attribute, CardInstance, FinalizationCard, OutcomeKind, RedCard


@dataclass(slots=True)
class Player:
    """Jugador de campo con un único atributo (DEF, MED o AT).

    ``value`` es su aportación individual a ese atributo del equipo.
    ``sent_off`` se activa con una tarjeta roja directa o con la segunda
    amarilla del partido; a partir de ese momento deja de sumar al equipo.
    """

    attribute: Attribute
    value: int
    yellow_cards: int = 0
    sent_off: bool = False


PLAYER_MIN_LEVEL = 1
PLAYER_MAX_LEVEL = 9


def _random_partition(
    total: int,
    parts: int,
    rng: random.Random,
    *,
    min_value: int = PLAYER_MIN_LEVEL,
    max_value: int = PLAYER_MAX_LEVEL,
) -> list[int]:
    """Reparte ``total`` en ``parts`` niveles al azar, entre ``min_value`` y ``max_value``.

    Si el reparto exacto no cabe en ese rango (caso extremo con totales fuera
    de lo habitual), se relaja el límite mínimo indispensable para que la
    suma siga cuadrando en lugar de fallar.
    """

    if parts <= 0:
        raise ValueError("El número de jugadores debe ser mayor que cero.")
    lo, hi = min_value, max_value
    if parts * lo > total:
        lo = total // parts
    if parts * hi < total:
        hi = -(-total // parts)
    values = [lo] * parts
    remaining = total - lo * parts
    while remaining > 0:
        index = rng.randrange(parts)
        if values[index] < hi:
            values[index] += 1
            remaining -= 1
    rng.shuffle(values)
    return values


# Únicas formas de repartir 7 jugadores en 3 categorías con máximo 3 por una.
_CATEGORY_SHAPES: tuple[tuple[int, int, int], ...] = (
    (3, 3, 1),
    (3, 1, 3),
    (1, 3, 3),
    (3, 2, 2),
    (2, 3, 2),
    (2, 2, 3),
)


def _feasible_counts(total: int) -> set[int]:
    """Cuenta de jugadores (1-3) con los que ``total`` cabe en niveles 1-9."""

    return {
        count
        for count in (1, 2, 3)
        if count * PLAYER_MIN_LEVEL <= total <= count * PLAYER_MAX_LEVEL
    }


def _shape_cost(total: int, count: int) -> int:
    """Cu\u00e1nto se sale ``total`` del rango 1-9 por jugador con ``count`` jugadores."""

    return max(0, total - count * PLAYER_MAX_LEVEL, count * PLAYER_MIN_LEVEL - total)


def generate_players(
    defense: int, midfield: int, attack: int, rng: random.Random
) -> tuple[Player, ...]:
    """Genera los 7 jugadores de un equipo (cada uno con un único atributo).

    Ninguna categoría tiene más de 3 jugadores; el valor de cada uno se
    reparte al azar, siempre entre nivel 1 y nivel 9, de forma que la suma
    por categoría coincide con el total del equipo (DEF, MED o AT). Si algún
    total es tan extremo que ninguna combinación cabe perfectamente entre 1
    y 9, se elige la combinación que menos se sale de ese rango.
    """

    feasible_def = _feasible_counts(defense)
    feasible_med = _feasible_counts(midfield)
    feasible_at = _feasible_counts(attack)
    valid_shapes = [
        shape
        for shape in _CATEGORY_SHAPES
        if shape[0] in feasible_def and shape[1] in feasible_med and shape[2] in feasible_at
    ]
    if valid_shapes:
        chosen_shapes = valid_shapes
    else:
        costs = [
            _shape_cost(defense, shape[0]) + _shape_cost(midfield, shape[1]) + _shape_cost(attack, shape[2])
            for shape in _CATEGORY_SHAPES
        ]
        best_cost = min(costs)
        chosen_shapes = [
            shape for shape, cost in zip(_CATEGORY_SHAPES, costs) if cost == best_cost
        ]
    def_count, med_count, at_count = rng.choice(chosen_shapes)
    players: list[Player] = []
    for attribute, total, count in (
        (Attribute.DEF, defense, def_count),
        (Attribute.MED, midfield, med_count),
        (Attribute.AT, attack, at_count),
    ):
        for value in _random_partition(total, count, rng):
            players.append(Player(attribute=attribute, value=value))
    return tuple(players)


@dataclass(frozen=True, slots=True)
class Team:
    """Atributos permanentes de un equipo y, opcionalmente, su plantilla de 7 jugadores.

    ``defense``/``midfield``/``attack`` son los totales nominales (los que se
    usan para configurar el partido). Cuando ``players`` está poblado,
    :meth:`value` refleja el total en vivo: los jugadores expulsados dejan de
    sumar a su categoría.
    """

    defense: int
    midfield: int
    attack: int
    players: tuple[Player, ...] = ()

    def __post_init__(self) -> None:
        if min(self.defense, self.midfield, self.attack) < 0:
            raise ValueError("DEF, MED y AT no pueden ser negativos.")

    def value(self, attribute: Attribute) -> int:
        if self.players:
            return sum(
                player.value
                for player in self.players
                if player.attribute is attribute and not player.sent_off
            )
        return {
            Attribute.DEF: self.defense,
            Attribute.MED: self.midfield,
            Attribute.AT: self.attack,
        }[attribute]


def _cloned_team(team: Team) -> Team:
    """Copia un equipo con jugadores nuevos (mismos datos, otra identidad).

    Necesario para explorar ramas especulativas sin mutar a los jugadores
    reales del partido: ``Team`` es inmutable, pero ``Player`` no lo es.
    """

    if not team.players:
        return team
    return replace(team, players=tuple(replace(player) for player in team.players))


def format_lineup(team: Team) -> str:
    """Muestra la alineación de 7 jugadores agrupada por atributo.

    Los expulsados aparecen tachados; no dejan de listarse para que se vea
    quién falta respecto al inicio del partido.
    """

    if not team.players:
        return "sin plantilla individual"
    groups: dict[Attribute, list[Player]] = {
        Attribute.DEF: [],
        Attribute.MED: [],
        Attribute.AT: [],
    }
    for player in team.players:
        groups[player.attribute].append(player)
    parts: list[str] = []
    for attribute in (Attribute.DEF, Attribute.MED, Attribute.AT):
        members = sorted(groups[attribute], key=lambda p: p.value, reverse=True)
        if not members:
            continue
        values = ", ".join(
            f"~~{member.value}~~" if member.sent_off else str(member.value)
            for member in members
        )
        parts.append(f"{attribute.value} ({len(members)}): {values}")
    return " · ".join(parts)


@dataclass(frozen=True, slots=True)
class MatchRules:
    """Reglas de flujo configurables que no forman parte de una carta."""

    ties_succeed: bool = False
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
    """Resultado seleccionado al resolver una CF y su condicional independiente.

    Los campos de modificador temporal registran, si existió, el atributo
    afectado durante las comparaciones de esta CF. El equipo nunca se muta para
    conservar ese modificador.
    """

    card_name: str
    outcome_name: str
    outcome_kind: OutcomeKind
    tier: int
    conditional_met: bool = False
    temporary_player_attribute: Attribute | None = None
    temporary_player_modifier: int = 0
    temporary_opponent_attribute: Attribute | None = None
    temporary_opponent_modifier: int = 0


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
    también se aplicó el efecto de la esquina inferior izquierda.
    ``temporary_opponent_attribute`` y ``temporary_opponent_modifier`` registran
    el modificador temporal usado únicamente para las comparaciones de esta CR.
    El resto de campos son una fotografía del estado justo tras resolver esta CR.
    """

    card: RedCard
    applied_action_index: int | None
    conditional_met: bool
    temporary_opponent_attribute: Attribute | None
    temporary_opponent_modifier: int
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
    discard_remaining: int
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
    used_jokes: set[str] = field(default_factory=set, repr=False)

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

        Los jugadores de la plantilla se clonan aparte: algunas estrategias
        (como :class:`OneNilLowCRAI`) aplican de verdad efectos de CC sobre
        esta copia para explorar variantes, y sin esta clonación una amarilla
        o expulsión especulativa mutaría a los jugadores reales del partido.
        """

        return MatchState(
            player=_cloned_team(self.player),
            opponent=_cloned_team(self.opponent),
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

    def decision_signature(self) -> tuple[tuple[str, ...], int, int, int, int, int]:
        """Estado relevante para una decisión local antes de una CF.

        El marcador también forma parte de la posición porque una CC puede tener
        un modificador condicional que depende de si el bot está ganando o perdiendo.
        """

        return (
            tuple(sorted(instance.card.definition_id for instance in self.hand)),
            self.pending_cc_bonus,
            self.pending_cf_bonus,
            self.pressure,
            self.player_goals,
            self.bot_goals,
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
