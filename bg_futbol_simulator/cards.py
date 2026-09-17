"""Definiciones inmutables de las cartas del sistema de partido.

Este módulo contiene datos de reglas, no lógica de resolución. Mantener las
cartas declarativas permite ampliar el mazo sin modificar el motor.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TypeAlias


class Attribute(str, Enum):
    """Atributos que pueden intervenir en una comparación."""

    DEF = "DEF"
    MED = "MED"
    AT = "AT"


class OutcomeKind(str, Enum):
    """Resultados visibles de una carta de finalización."""

    GOAL = "gol"
    NOTHING = "nada"
    PRESSURE_INCREASE = "aumento de presión"
    PRESSURE_REDUCTION = "reducción de presión"
    RED_CARD = "tarjeta roja"
    YELLOW_CARD = "tarjeta amarilla"
    CR_DRAW = "roba CR"


@dataclass(frozen=True, slots=True)
class Comparison:
    """Prueba ``atributo jugador`` contra ``atributo rival + modificador``."""

    player_attribute: Attribute
    opponent_attribute: Attribute
    opponent_modifier: int = 0
    ties_succeed: bool | None = None


@dataclass(frozen=True, slots=True)
class Effect:
    """Cambio atómico que puede producir una opción de carta.

    Los campos son aditivos. ``discard_top_cards`` descarta cartas del mazo sin
    resolverlas; esto preserva exactamente el significado de "descarta la
    primera carta del mazo".
    """

    cc_bonus: int = 0
    cf_bonus: int = 0
    pressure_delta: int = 0
    discard_top_cards: int = 0
    discard_control_cards: int = 0
    goals: int = 0
    bot_goals: int = 0
    cr_draws: int = 0
    yellow_cards: int = 0
    red_cards: int = 0
    player_yellow_cards: int = 0
    player_red_cards: int = 0
    yellow_injury_rolls: int = 0
    red_injury_rolls: int = 0
    draw_main_cards: int = 0
    recover_control_cards: int = 0
    play_random_discard_finalizations: int = 0
    draw_red_cards: int = 0


@dataclass(frozen=True, slots=True)
class ControlOption:
    """Una de las tres elecciones de una CC."""

    key: str
    label: str
    effect: Effect
    comparison: Comparison | None = None

    @property
    def requires_comparison(self) -> bool:
        return self.comparison is not None


@dataclass(frozen=True, slots=True)
class ControlCard:
    """Carta de control (CC) que va a la mano del jugador."""

    definition_id: str
    name: str
    copies: int
    options: tuple[ControlOption, ...]

    def option(self, key: str) -> ControlOption:
        for option in self.options:
            if option.key == key:
                return option
        raise KeyError(f"La carta {self.name!r} no tiene la opción {key!r}.")


@dataclass(frozen=True, slots=True)
class FinalizationOutcome:
    """Resultado ordenado de una CF.

    ``tier`` expresa la prioridad de IA: 2 es el mejor resultado, 1 el
    intermedio y 0 el resultado de no conseguir ninguna comparación.
    """

    name: str
    kind: OutcomeKind
    tier: int
    effect: Effect
    comparison: Comparison | None = None


@dataclass(frozen=True, slots=True)
class FinalizationCard:
    """Carta de finalización (CF) resuelta tras jugar las CC deseadas."""

    definition_id: str
    name: str
    copies: int
    outcomes: tuple[
        FinalizationOutcome, FinalizationOutcome, FinalizationOutcome
    ]


@dataclass(frozen=True, slots=True)
class EventOption:
    """Una de las tres decisiones disponibles al revelar una CE."""

    key: str
    label: str
    effect: Effect


@dataclass(frozen=True, slots=True)
class EventCard:
    """Carta de evento (CE) que se resuelve inmediatamente."""

    definition_id: str
    name: str
    copies: int
    options: tuple[EventOption, EventOption, EventOption]

    def option(self, key: str) -> EventOption:
        for option in self.options:
            if option.key == key:
                return option
        raise KeyError(f"El evento {self.name!r} no tiene la opción {key!r}.")


class RivalCondition(str, Enum):
    """Estado del marcador que activa la acción de la esquina inferior izquierda."""

    RIVAL_WINNING = "el rival está ganando"
    RIVAL_LOSING = "el rival está perdiendo"


@dataclass(frozen=True, slots=True)
class RedComparison:
    """Compara un atributo del rival contra uno propio (más un margen).

    Por defecto la acción se activa si el atributo rival supera al propio más
    el margen (``rival_attribute > player_attribute + player_modifier``).
    ``rival_must_be_lower`` invierte el sentido de la comparación.
    """

    rival_attribute: Attribute
    player_attribute: Attribute
    player_modifier: int = 0
    rival_must_be_lower: bool = False


@dataclass(frozen=True, slots=True)
class RedCardAction:
    """Una de las dos primeras acciones de una CR (arriba), por comparación."""

    label: str
    comparison: RedComparison
    effect: Effect


@dataclass(frozen=True, slots=True)
class RedCardConditional:
    """Acción de la esquina inferior izquierda de una CR.

    Se aplica siempre que se cumpla su condición de marcador, de forma
    independiente a la acción principal (pudiendo sumarse ambos efectos).
    """

    label: str
    condition: RivalCondition
    effect: Effect


@dataclass(frozen=True, slots=True)
class RedCard:
    """Carta roja (CR) que sustituye al antiguo contador de CR.

    Se aplica una única acción obligatoria recorriendo la carta de arriba
    hacia abajo: la primera de las dos acciones cuya comparación se cumpla: si
    ninguna se cumple, se aplica ``fallback_effect`` (esquina inferior
    derecha, sin condición). Además, y de forma independiente, si se cumple
    la condición de marcador de ``conditional`` (esquina inferior izquierda)
    se aplica también su efecto: una misma carta puede así producir dos
    efectos consecutivos.
    """

    definition_id: str
    name: str
    copies: int
    actions: tuple[RedCardAction, RedCardAction]
    fallback_effect: Effect
    conditional: RedCardConditional


CardDefinition: TypeAlias = ControlCard | FinalizationCard | EventCard | RedCard


@dataclass(frozen=True, slots=True)
class CardInstance:
    """Una copia identificable de una definición de carta."""

    instance_id: str
    card: CardDefinition


def _control(
    definition_id: str,
    name: str,
    copies: int,
    base: Effect,
    comparison_1: Comparison,
    reward_1: Effect,
    comparison_2: Comparison,
    reward_2: Effect,
) -> ControlCard:
    return ControlCard(
        definition_id=definition_id,
        name=name,
        copies=copies,
        options=(
            ControlOption("base", "Efecto base", base),
            ControlOption("comparison_1", "Comparación 1", reward_1, comparison_1),
            ControlOption("comparison_2", "Comparación 2", reward_2, comparison_2),
        ),
    )


def control_card_definitions() -> tuple[ControlCard, ...]:
    """Devuelve las diez definiciones del mazo definitivo de 28 CC."""

    return (
        _control(
            "build_from_back",
            "Construcción desde atrás",
            4,
            Effect(cc_bonus=2),
            Comparison(Attribute.MED, Attribute.DEF),
            Effect(cc_bonus=4),
            Comparison(Attribute.DEF, Attribute.MED, 1),
            Effect(cf_bonus=2),
        ),
        _control(
            "aggressive_recovery",
            "Recuperación agresiva",
            4,
            Effect(cc_bonus=2),
            Comparison(Attribute.DEF, Attribute.MED),
            Effect(pressure_delta=-2),
            Comparison(Attribute.MED, Attribute.MED),
            Effect(yellow_cards=1, cf_bonus=3),
        ),
        _control(
            "wing_play",
            "Apertura a banda",
            3,
            Effect(cf_bonus=1),
            Comparison(Attribute.MED, Attribute.DEF, 2),
            Effect(cf_bonus=3),
            Comparison(Attribute.MED, Attribute.MED, 1),
            Effect(cc_bonus=3),
        ),
        _control(
            "through_ball",
            "Balón al espacio",
            3,
            Effect(cf_bonus=2, pressure_delta=1),
            Comparison(Attribute.MED, Attribute.DEF, 2),
            Effect(cf_bonus=3),
            Comparison(Attribute.AT, Attribute.DEF, 2),
            Effect(cc_bonus=4),
        ),
        _control(
            "one_two",
            "Triangulación de equipo",
            3,
            Effect(cc_bonus=2),
            Comparison(Attribute.MED, Attribute.MED, 1),
            Effect(cc_bonus=4),
            Comparison(Attribute.AT, Attribute.MED, 1),
            Effect(cf_bonus=2),
        ),
        _control(
            "cross_into_box",
            "Centro al área",
            3,
            Effect(cf_bonus=1),
            Comparison(Attribute.MED, Attribute.DEF, 1),
            Effect(cf_bonus=2),
            Comparison(Attribute.AT, Attribute.DEF, 3),
            Effect(cf_bonus=3),
        ),
        _control(
            "switch_of_play",
            "Cambio de orientación",
            2,
            Effect(cc_bonus=2, discard_top_cards=1),
            Comparison(Attribute.MED, Attribute.MED, 3),
            Effect(cf_bonus=3),
            Comparison(Attribute.MED, Attribute.DEF, 2),
            Effect(pressure_delta=-1, cf_bonus=1),
        ),
        _control(
            "line_breaking_pass",
            "Pase entre líneas",
            2,
            Effect(cc_bonus=2),
            Comparison(Attribute.MED, Attribute.DEF, 3),
            Effect(cf_bonus=3),
            Comparison(Attribute.AT, Attribute.DEF),
            Effect(cc_bonus=3),
        ),
        _control(
            "individual_action",
            "Acción individual",
            2,
            Effect(cf_bonus=1),
            Comparison(Attribute.AT, Attribute.DEF, 1),
            Effect(cf_bonus=1, yellow_cards=1),
            Comparison(Attribute.AT, Attribute.DEF, 4),
            Effect(cf_bonus=4),
        ),
        _control(
            "game_control",
            "Control del juego",
            2,
            Effect(cc_bonus=2),
            Comparison(Attribute.MED, Attribute.MED, 2),
            Effect(pressure_delta=-2, cc_bonus=2),
            Comparison(Attribute.MED, Attribute.MED),
            Effect(pressure_delta=-1, cc_bonus=2),
        ),
    )


def _finalization(
    definition_id: str,
    name: str,
    best: FinalizationOutcome,
    middle: FinalizationOutcome,
    fallback: FinalizationOutcome,
) -> FinalizationCard:
    return FinalizationCard(definition_id, name, 2, (best, middle, fallback))


def finalization_card_definitions() -> tuple[FinalizationCard, ...]:
    """Devuelve las seis definiciones del mazo definitivo de 12 CF."""

    def strict_comparison(
        player_attribute: Attribute, opponent_attribute: Attribute, modifier: int = 0
    ) -> Comparison:
        """Las CF actualizadas usan `>`: un empate no supera la prueba."""

        return Comparison(player_attribute, opponent_attribute, modifier, ties_succeed=False)

    high_goal = lambda attribute, modifier: FinalizationOutcome(
        "Gol", OutcomeKind.GOAL, 2, Effect(goals=1),
        strict_comparison(attribute, Attribute.DEF, modifier),
    )
    cr = lambda: FinalizationOutcome("Roba 1 CR", OutcomeKind.CR_DRAW, 0, Effect(cr_draws=1))
    nothing = lambda tier=0: FinalizationOutcome("Nada", OutcomeKind.NOTHING, tier, Effect())

    return (
        _finalization(
            "one_on_one", "Mano a mano", high_goal(Attribute.AT, 4),
            FinalizationOutcome(
                "Descarta 1 CC de la mano y +2 Presión",
                OutcomeKind.PRESSURE_REDUCTION,
                1,
                Effect(discard_control_cards=1, pressure_delta=2),
                strict_comparison(Attribute.AT, Attribute.DEF),
            ),
            cr(),
        ),
        _finalization(
            "cutback", "Ultimo pase", high_goal(Attribute.MED, 4),
            FinalizationOutcome("+1 Presión", OutcomeKind.PRESSURE_REDUCTION, 1, Effect(pressure_delta=1), strict_comparison(Attribute.MED, Attribute.DEF, 2)),
            cr(),
        ),
        _finalization(
            "header", "Remate de cabeza", high_goal(Attribute.AT, 4),
            FinalizationOutcome(
                "Descarta la primera carta del mazo y +1 Presión",
                OutcomeKind.PRESSURE_REDUCTION,
                1,
                Effect(discard_top_cards=1, pressure_delta=1),
                strict_comparison(Attribute.AT, Attribute.DEF, 1),
            ),
            FinalizationOutcome(
                "Roba 1 CR y -1 Presión",
                OutcomeKind.CR_DRAW,
                0,
                Effect(cr_draws=1, pressure_delta=-1),
            ),
        ),
        _finalization(
            "long_shot", "Disparo lejano", high_goal(Attribute.AT, 4),
            FinalizationOutcome(
                "+2 Presión",
                OutcomeKind.PRESSURE_REDUCTION,
                1,
                Effect(pressure_delta=2),
                strict_comparison(Attribute.AT, Attribute.DEF, 1),
            ),
            FinalizationOutcome(
                "Descarta una CC de la mano y roba 1 CR",
                OutcomeKind.CR_DRAW,
                0,
                Effect(discard_control_cards=1, cr_draws=1),
            ),
        ),
        _finalization(
            "win_corner", "Buscar el córner",
            FinalizationOutcome(
                "-2 Presión",
                OutcomeKind.PRESSURE_REDUCTION,
                2,
                Effect(pressure_delta=-3),
                strict_comparison(Attribute.MED, Attribute.DEF, 3),
            ),
            FinalizationOutcome(
                "+2 Presión",
                OutcomeKind.PRESSURE_REDUCTION,
                1,
                Effect(pressure_delta=2),
                strict_comparison(Attribute.MED, Attribute.DEF, 1),
            ),
            FinalizationOutcome(
                "+3 Presión y descarta una CC de la mano",
                OutcomeKind.PRESSURE_INCREASE,
                0,
                Effect(pressure_delta=3, discard_control_cards=1),
            ),
        ),
        _finalization(
            "draw_foul", "Provocar la falta",
            FinalizationOutcome(
                "Tarjeta roja y descarta una carta del mazo",
                OutcomeKind.RED_CARD,
                2,
                Effect(red_cards=1, discard_top_cards=1),
                strict_comparison(Attribute.AT, Attribute.DEF, 6),
            ),
            FinalizationOutcome(
                "Tarjeta amarilla y +2 Presión",
                OutcomeKind.YELLOW_CARD,
                1,
                Effect(yellow_cards=1, pressure_delta=2),
                strict_comparison(Attribute.AT, Attribute.DEF),
            ),
            FinalizationOutcome(
                "Roba 1 CR y descarta la primera carta del mazo",
                OutcomeKind.CR_DRAW,
                0,
                Effect(cr_draws=1, discard_top_cards=1),
            ),
        ),
    )


def _event(
    definition_id: str,
    name: str,
    copies: int,
    first: Effect,
    second: Effect,
    third: Effect,
) -> EventCard:
    return EventCard(
        definition_id=definition_id,
        name=name,
        copies=copies,
        options=(
            EventOption("option_1", "Opción 1", first),
            EventOption("option_2", "Opción 2", second),
            EventOption("option_3", "Opción 3", third),
        ),
    )


def event_card_definitions() -> tuple[EventCard, ...]:
    """Devuelve las cinco definiciones oficiales de 10 CE v1.0."""

    return (
        _event(
            "time_wasting",
            "Pérdida de tiempo",
            3,
            Effect(discard_top_cards=2, pressure_delta=1, yellow_cards=1),
            Effect(cr_draws=1, discard_control_cards=1, pressure_delta=-4),
            Effect(pressure_delta=1, yellow_injury_rolls=1, discard_top_cards=1),
        ),
        _event(
            "offside",
            "Fuera de juego",
            3,
            Effect(discard_top_cards=1, discard_control_cards=2),
            Effect(pressure_delta=2),
            Effect(cr_draws=1, pressure_delta=-3),
        ),
        _event(
            "advantage_rule",
            "Ley de la ventaja",
            2,
            Effect(yellow_cards=1, pressure_delta=3),
            Effect(discard_top_cards=1, yellow_injury_rolls=1, pressure_delta=1),
            Effect(player_yellow_cards=1, yellow_injury_rolls=1, pressure_delta=-1),
        ),
        _event(
            "var",
            "VAR",
            1,
            Effect(yellow_cards=1, pressure_delta=3),
            Effect(cr_draws=1, pressure_delta=-3),
            Effect(recover_control_cards=1, pressure_delta=2),
        ),
        _event(
            "corner_event",
            "Córner",
            1,
            Effect(play_random_discard_finalizations=1, pressure_delta=2),
            Effect(draw_main_cards=1, pressure_delta=1),
            Effect(discard_top_cards=1, pressure_delta=1),
        ),
    )


def weak_team_support_card() -> ControlCard:
    """CC de equilibrio: se añade una copia por cada 10 puntos que el equipo
    del jugador quede por debajo del rival (suma de DEF+MED+AT). Solo tiene
    dos opciones, ambas sin comparación, siempre jugables.
    """

    return ControlCard(
        definition_id="fuerza_del_debil",
        name="La fuerza del débil",
        copies=0,
        options=(
            ControlOption("option_1", "Opción 1", Effect(pressure_delta=-2, cc_bonus=4)),
            ControlOption("option_2", "Opción 2", Effect(cf_bonus=4)),
        ),
    )


def strong_team_handicap_card() -> EventCard:
    """CE de equilibrio: se añade una copia por cada 10 puntos que el equipo
    del jugador supere al rival (suma de DEF+MED+AT).
    """

    return _event(
        "fuerza_rival_debil",
        "La fuerza del rival Débil",
        0,
        Effect(discard_top_cards=2, pressure_delta=6),
        Effect(discard_top_cards=1, pressure_delta=2, cr_draws=1),
        Effect(discard_top_cards=1, red_injury_rolls=1, pressure_delta=5),
    )


def _red_action(
    rival_attribute: Attribute,
    player_attribute: Attribute,
    player_modifier: int,
    effect: Effect,
    *,
    rival_must_be_lower: bool = False,
) -> RedCardAction:
    operator = "<" if rival_must_be_lower else ">"
    modifier_text = f" +{player_modifier}" if player_modifier else ""
    return RedCardAction(
        label=f"{rival_attribute.value} rival {operator} {player_attribute.value} jugador{modifier_text}",
        comparison=RedComparison(
            rival_attribute, player_attribute, player_modifier, rival_must_be_lower
        ),
        effect=effect,
    )


def _red_conditional(condition: RivalCondition, effect: Effect) -> RedCardConditional:
    return RedCardConditional(
        label=f"Si {condition.value}", condition=condition, effect=effect
    )


def _red_card(
    definition_id: str,
    name: str,
    action_1: RedCardAction,
    action_2: RedCardAction,
    fallback_effect: Effect,
    conditional: RedCardConditional,
) -> RedCard:
    return RedCard(
        definition_id=definition_id,
        name=name,
        copies=2,
        actions=(action_1, action_2),
        fallback_effect=fallback_effect,
        conditional=conditional,
    )


def red_card_definitions() -> tuple[RedCard, ...]:
    """Devuelve las ocho definiciones del mazo de 16 CR (dos copias cada una).

    Cada CR compara un atributo del rival contra un atributo del jugador (más
    su modificador). Se recorre la carta de arriba hacia abajo aplicando una
    única acción obligatoria: la primera de las dos acciones cuya comparación
    se cumpla o, si ninguna se cumple, el efecto de reserva (esquina inferior
    derecha, sin condición). Además, de forma independiente, si se cumple la
    condición de marcador de la esquina inferior izquierda se aplica también
    su efecto.
    """

    return (
        _red_card(
            "ataque_banda",
            "Ataque por banda",
            _red_action(Attribute.MED, Attribute.DEF, 2, Effect(pressure_delta=6)),
            _red_action(Attribute.MED, Attribute.MED, 1, Effect(pressure_delta=5)),
            Effect(pressure_delta=4),
            _red_conditional(
                RivalCondition.RIVAL_WINNING,
                Effect(discard_top_cards=1),
            ),
        ),
        _red_card(
            "control_posesion",
            "Control de la posesión",
            _red_action(
                Attribute.MED, Attribute.MED, 3,
                Effect(discard_control_cards=1, pressure_delta=5),
            ),
            _red_action(
                Attribute.MED, Attribute.MED, 2,
                Effect(discard_control_cards=1, pressure_delta=4),
            ),
            Effect(discard_control_cards=1, pressure_delta=2),
            _red_conditional(
                RivalCondition.RIVAL_WINNING,
                Effect(discard_top_cards=1),
            ),
        ),
        _red_card(
            "accion_individual_rival",
            "Acción rival individual",
            _red_action(Attribute.AT, Attribute.DEF, 3, Effect(bot_goals=1)),
            _red_action(
                Attribute.AT, Attribute.DEF, 1,
                Effect(player_yellow_cards=1, pressure_delta=3),
            ),
            Effect(discard_top_cards=1, player_yellow_cards=1, pressure_delta=1),
            _red_conditional(
                RivalCondition.RIVAL_LOSING,
                Effect(pressure_delta=1),
            ),
        ),
        _red_card(
            "balon_parado",
            "Balón parado",
            _red_action(Attribute.AT, Attribute.DEF, 4, Effect(bot_goals=1)),
            _red_action(Attribute.AT, Attribute.DEF, 2, Effect(pressure_delta=5)),
            Effect(pressure_delta=3),
            _red_conditional(
                RivalCondition.RIVAL_WINNING,
                Effect(discard_top_cards=1),
            ),
        ),
        _red_card(
            "centro_area_rival",
            "Centro al área",
            _red_action(Attribute.MED, Attribute.DEF, 4, Effect(pressure_delta=6)),
            _red_action(Attribute.AT, Attribute.DEF, 1, Effect(pressure_delta=4)),
            Effect(pressure_delta=3),
            _red_conditional(
                RivalCondition.RIVAL_LOSING,
                Effect(pressure_delta=1),
            ),
        ),
        _red_card(
            "robo_mediocampo",
            "Robo en medio campo",
            _red_action(Attribute.DEF, Attribute.MED, 3, Effect(pressure_delta=5)),
            _red_action(Attribute.MED, Attribute.MED, 3, Effect(pressure_delta=5)),
            Effect(pressure_delta=3),
            _red_conditional(
                RivalCondition.RIVAL_LOSING,
                Effect(discard_control_cards=2),
            ),
        ),
        _red_card(
            "contraataque_rival",
            "Contraataque rival",
            _red_action(
                Attribute.AT, Attribute.MED, 3,
                Effect(recover_control_cards=1, bot_goals=1),
            ),
            _red_action(
                Attribute.AT, Attribute.MED, 0,
                Effect(pressure_delta=1, draw_red_cards=1),
            ),
            Effect(pressure_delta=4, recover_control_cards=1),
            _red_conditional(
                RivalCondition.RIVAL_WINNING,
                Effect(player_yellow_cards=1),
            ),
        ),
        _red_card(
            "pase_cortado",
            "Pase cortado",
            _red_action(
                Attribute.MED, Attribute.AT, 4,
                Effect(recover_control_cards=1, pressure_delta=4),
            ),
            _red_action(Attribute.MED, Attribute.MED, 2, Effect(pressure_delta=5)),
            Effect(pressure_delta=3),
            _red_conditional(
                RivalCondition.RIVAL_LOSING,
                Effect(discard_control_cards=1),
            ),
        ),
    )


def build_red_card_deck() -> list[CardInstance]:
    """Crea las 16 copias del mazo de CR (8 tipos × 2 copias), sin barajar."""

    instances: list[CardInstance] = []
    for card in red_card_definitions():
        for copy_number in range(1, card.copies + 1):
            instances.append(CardInstance(f"{card.definition_id}-{copy_number}", card))
    return instances


def red_card_catalogue() -> dict[str, RedCard]:
    """Índice por id de las CR, útil para interfaces y pruebas externas."""

    return {card.definition_id: card for card in red_card_definitions()}


def all_card_definitions() -> tuple[CardDefinition, ...]:
    return (
        *control_card_definitions(),
        *finalization_card_definitions(),
        *event_card_definitions(),
        weak_team_support_card(),
        strong_team_handicap_card(),
    )


def build_match_deck() -> list[CardInstance]:
    """Crea las 50 copias: 28 CC, 12 CF y 10 CE, aún sin barajar."""

    instances: list[CardInstance] = []
    for card in all_card_definitions():
        for copy_number in range(1, card.copies + 1):
            instances.append(CardInstance(f"{card.definition_id}-{copy_number}", card))
    return instances



def card_catalogue() -> dict[str, CardDefinition]:
    """Índice por id, útil para interfaces y pruebas externas."""

    return {card.definition_id: card for card in all_card_definitions()}
