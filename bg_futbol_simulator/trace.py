"""Genera informes Markdown reproducibles de un partido completo."""

from __future__ import annotations

import argparse
from pathlib import Path
from random import Random
from typing import TextIO

from .ai import AutomaticPlayerAI
from .cards import Comparison, ControlCard, Effect, EventCard, FinalizationCard, RedComparison
from .engine import RulesEngine
from .game_state import MatchState, RedCardResolution, Team
from .strategies import OneNilLowCRAI


def _effect_text(effect: Effect) -> str:
    parts: list[str] = []
    values = (
        (effect.cc_bonus, "CC"),
        (effect.cf_bonus, "CF"),
        (effect.pressure_delta, "Presión"),
        (effect.goals, "gol del jugador"),
        (effect.bot_goals, "gol en contra"),
        (effect.cr_draws, "CR"),
        (effect.yellow_cards, "amarilla rival"),
        (effect.red_cards, "roja rival"),
        (effect.player_yellow_cards, "amarilla propia"),
        (effect.player_red_cards, "roja propia"),
    )
    for value, label in values:
        if value:
            parts.append(f"{value:+d} {label}")
    if effect.yellow_injury_rolls:
        parts.append("tirada de lesión por amarilla (10%)")
    if effect.red_injury_rolls:
        parts.append("tirada de lesión por roja (15%)")
    if effect.draw_main_cards:
        parts.append(f"roba {effect.draw_main_cards} carta del mazo")
    if effect.discard_top_cards:
        parts.append(f"descarta {effect.discard_top_cards} carta(s) del mazo")
    if effect.discard_control_cards:
        parts.append(f"descarta {effect.discard_control_cards} CC de la mano")
    if effect.recover_control_cards:
        parts.append("recupera 1 CC del descarte")
    if effect.play_random_discard_finalizations:
        parts.append("juega una CF aleatoria del descarte")
    if effect.draw_red_cards:
        parts.append(f"juega {effect.draw_red_cards} CR adicional(es)")
    return "; ".join(parts) or "sin efecto adicional"


def _comparison_text(state: MatchState, comparison: Comparison, bonus: int) -> str:
    player = state.player.value(comparison.player_attribute) + bonus
    opponent = state.opponent.value(comparison.opponent_attribute) + comparison.opponent_modifier
    operator = ">=" if (comparison.ties_succeed is not False) else ">"
    return (
        f"{comparison.player_attribute.value} jugador {player} {operator} "
        f"{comparison.opponent_attribute.value} rival {opponent}"
    )


def _finalization_comparison_text(
    state: MatchState, comparison: Comparison, bonus_parts: list[int]
) -> str:
    """Desglosa la comparación de CF con cada +CF jugado antes de resolverla."""

    base_value = state.player.value(comparison.player_attribute)
    total_bonus = state.pending_cf_bonus
    pieces = [str(base_value), *(_green_bonus(bonus) for bonus in bonus_parts if bonus)]
    displayed_total = sum(bonus_parts)
    if total_bonus != displayed_total:
        pieces.append(_green_bonus(total_bonus - displayed_total))
    player_value = base_value + total_bonus
    opponent_base = state.opponent.value(comparison.opponent_attribute)
    opponent_value = opponent_base + comparison.opponent_modifier
    opponent = (
        str(opponent_base)
        if comparison.opponent_modifier == 0
        else f"{opponent_base} {comparison.opponent_modifier:+d} = {opponent_value}"
    )
    operator = ">=" if (comparison.ties_succeed is not False) else ">"
    return (
        f"{comparison.player_attribute.value} jugador {' '.join(pieces)} = {player_value} "
        f"{operator} {comparison.opponent_attribute.value} rival {opponent}"
    )


def _red_comparison_text(state: MatchState, comparison: RedComparison) -> str:
    """Desglosa la comparación rival-vs-jugador de una acción de CR."""

    rival_value = state.opponent.value(comparison.rival_attribute)
    player_base = state.player.value(comparison.player_attribute)
    player_value = player_base + comparison.player_modifier
    player_text = (
        str(player_base)
        if comparison.player_modifier == 0
        else f"{player_base} {comparison.player_modifier:+d} = {player_value}"
    )
    operator = "<" if comparison.rival_must_be_lower else ">"
    return (
        f"{comparison.rival_attribute.value} rival {rival_value} {operator} "
        f"{comparison.player_attribute.value} jugador {player_text}"
    )


def _green_bonus(value: int) -> str:
    """Bono de CC en línea, compatible con el visor Markdown de Codex."""

    return f"🟢 **{value:+d}**"


def _hand_text(state: MatchState) -> str:
    return ", ".join(instance.card.name for instance in state.hand) or "—"


def _hand_indicator(state: MatchState) -> str:
    """Muestra el número de CC y una ficha verde por cada carta en mano."""

    count = len(state.hand)
    squares = " ".join("🟩" for _ in range(count))
    return f"{count}/{state.rules.max_control_hand_size}" + (f" {squares}" if squares else "")


def _deck_remaining_text(state: MatchState) -> str:
    """Cuenta las cartas que aún quedan por robar del mazo de partido."""

    control = sum(isinstance(instance.card, ControlCard) for instance in state.deck)
    finalization = sum(isinstance(instance.card, FinalizationCard) for instance in state.deck)
    event = sum(isinstance(instance.card, EventCard) for instance in state.deck)
    red = len(state.red_deck) + len(state.red_discard_pile)
    return f"mazo restante: {control} CC, {finalization} CF y {event} CE; CR disponibles: {red}"


def _summary_text(
    player_goals: int,
    bot_goals: int,
    pressure: int,
    pending_cc_bonus: int,
    pending_cf_bonus: int,
    cr_draws: int,
    hand_indicator: str,
    deck_remaining_text: str,
) -> str:
    return (
        f"Marcador jugador {player_goals}–{bot_goals} bot; "
        f"presión {pressure}; +CC {pending_cc_bonus}; "
        f"+CF {pending_cf_bonus}; CR {cr_draws}; mano {hand_indicator}; "
        f"{deck_remaining_text}."
    )


def _summary(state: MatchState) -> str:
    return _summary_text(
        state.player_goals,
        state.bot_goals,
        state.pressure,
        state.pending_cc_bonus,
        state.pending_cf_bonus,
        state.cr_draws,
        _hand_indicator(state),
        _deck_remaining_text(state),
    )


def _summary_from_red_card_resolution(resolution: RedCardResolution) -> str:
    """Formatea la fotografía tomada justo tras resolver una CR."""

    bot_goals = resolution.bot_goals_from_pressure + resolution.bot_goals_from_red_cards
    squares = " ".join("🟩" for _ in range(resolution.hand_size))
    hand_indicator = f"{resolution.hand_size}/{resolution.max_control_hand_size}" + (
        f" {squares}" if squares else ""
    )
    deck_remaining_text = (
        f"mazo restante: {resolution.control_remaining} CC, "
        f"{resolution.finalization_remaining} CF y {resolution.event_remaining} CE; "
        f"CR disponibles: {resolution.red_available}"
    )
    return _summary_text(
        resolution.player_goals,
        bot_goals,
        resolution.pressure,
        resolution.pending_cc_bonus,
        resolution.pending_cf_bonus,
        resolution.cr_draws,
        hand_indicator,
        deck_remaining_text,
    )


def _write_red_card_block(
    output: TextIO, state: MatchState, resolution: RedCardResolution
) -> str:
    """Muestra las cuatro acciones de una CR y marca las aplicadas.

    Se recorren, en orden: las dos acciones por comparación, la de reserva
    (aplicada solo si ninguna de las dos anteriores se cumple) y, de forma
    independiente, la condicionada al marcador (esquina inferior izquierda).
    Devuelve el texto del marcador resultante, para evitar repetirlo si nada
    más cambia antes del resumen del turno.
    """

    card = resolution.card
    print(f"- 🔴 CR ejecutada: **{card.name}**.", file=output)
    for index, action in enumerate(card.actions):
        description = (
            f"{_red_comparison_text(state, action.comparison)} → {_effect_text(action.effect)}."
        )
        if index == resolution.applied_action_index:
            print(f"  - **✅ Opción {index + 1}: {description}**", file=output)
        else:
            print(f"  - ⬜ Opción {index + 1}: {description}", file=output)
    fallback_description = (
        f"Ninguna acción anterior se cumple → {_effect_text(card.fallback_effect)}."
    )
    if resolution.applied_action_index is None:
        print(f"  - **✅ Opción de reserva: {fallback_description}**", file=output)
    else:
        print(f"  - ⬜ Opción de reserva: {fallback_description}", file=output)
    conditional_description = (
        f"{card.conditional.label} → {_effect_text(card.conditional.effect)}."
    )
    if resolution.conditional_met:
        print(
            f"  - **✅ Esquina inferior izquierda (independiente): {conditional_description}**",
            file=output,
        )
    else:
        print(
            f"  - ⬜ Esquina inferior izquierda (independiente): {conditional_description}",
            file=output,
        )
    summary = _summary_from_red_card_resolution(resolution)
    print(f"- {summary}", file=output)
    return summary


def _write_finalization_options(
    output: TextIO,
    state: MatchState,
    card: FinalizationCard,
    selected_outcome: object,
    bonus_parts: list[int],
) -> None:
    """Muestra los tres resultados posibles de una CF y marca el aplicado."""

    print("- 🟧 Opciones de la CF tras jugar las CC:", file=output)
    for number, outcome in enumerate(card.outcomes, 1):
        condition = (
            _finalization_comparison_text(state, outcome.comparison, bonus_parts)
            if outcome.comparison is not None
            else "Fallo: no se supera ninguna comparación anterior"
        )
        description = f"{condition} → {outcome.name}."
        if outcome == selected_outcome:
            print(f"  - **✅ Opción {number}: {description}**", file=output)
        else:
            print(f"  - ⬜ Opción {number}: {description}", file=output)


def _write_event_options(
    output: TextIO, card: EventCard, selected_option: object
) -> None:
    """Muestra las tres decisiones de una CE y marca la elegida por la IA."""

    print("- 🟪 Opciones de la CE:", file=output)
    for number, option in enumerate(card.options, 1):
        description = f"{_effect_text(option.effect)}."
        if option == selected_option:
            print(f"  - **✅ Opción {number}: {description}**", file=output)
        else:
            print(f"  - ⬜ Opción {number}: {description}", file=output)


def write_match_trace(
    seed: int,
    output: TextIO,
    *,
    strategy: str = "standard",
    player: Team | None = None,
    opponent: Team | None = None,
) -> None:
    """Ejecuta un partido con los equipos indicados y escribe su traza Markdown."""

    engine = RulesEngine()
    ai = OneNilLowCRAI(engine) if strategy == "one_nil_low_cr" else AutomaticPlayerAI(engine)
    player_team = player or Team(15, 15, 15)
    opponent_team = opponent or Team(15, 15, 15)
    state = engine.create_match_state(player_team, opponent_team, Random(seed))
    event_cursor = 0
    red_card_cursor = 0

    def line(text: str = "") -> None:
        print(text, file=output)

    def audit_events() -> None:
        nonlocal event_cursor
        for event in state.events[event_cursor:]:
            line(f"  - Registro: {event.detail}.")
        event_cursor = len(state.events)

    def audit_red_cards() -> str | None:
        nonlocal red_card_cursor
        last_summary = None
        for resolution in state.red_card_resolutions[red_card_cursor:]:
            last_summary = _write_red_card_block(output, state, resolution)
        red_card_cursor = len(state.red_card_resolutions)
        return last_summary

    def turn_summary(last_red_card_summary: str | None) -> None:
        """Evita repetir el marcador si ya se mostró en el último bloque de CR."""

        summary = _summary(state)
        if summary != last_red_card_summary:
            line(f"- {summary}")

    line("# Partido simulado paso a paso — BG FÚTBOL")
    line()
    line(f"- Semilla reproducible: `{seed}`")
    line(
        f"- Jugador: DEF {player_team.defense} · MED {player_team.midfield} "
        f"· AT {player_team.attack}"
    )
    line(
        f"- Bot: DEF {opponent_team.defense} · MED {opponent_team.midfield} "
        f"· AT {opponent_team.attack}"
    )
    line("- Mazo: 28 CC, 12 CF y 10 CE; mazo de CR aparte: 16 (8 tipos × 2)")
    line("- Mano inicial: 0 CC; límite: 5 CC")
    line("- Gol del bot: al superar presión 9, la presión vuelve a 0")
    line(
        "- Estrategia: "
        + (
            "buscar 1–0; conservar CC hasta 2 CR y después minimizar CR"
            if strategy == "one_nil_low_cr"
            else "IA estándar"
        )
    )
    line()
    line("## Leyenda visual")
    line()
    line("- 🟩 **CC** — carta de control: entra en la mano.")
    line("- 🟧 **CF** — carta de finalización: permite jugar CC y se resuelve.")
    line("- 🟪 **CE** — carta de evento: la IA elige una de sus tres opciones.")
    line("- 🔴 **CR** — carta roja: sustituye al contador de CR; se roba y se resuelve al instante.")
    line("- 🟢 **+n** — bono +CF que las CC aplican al atributo del jugador en una CF.")
    line()
    line("## Desarrollo completo")

    while (instance := engine.draw_next_card(state)) is not None:
        card = instance.card
        line()
        icon = "🟩" if isinstance(card, ControlCard) else "🟧" if isinstance(card, FinalizationCard) else "🟪"
        card_type = "CC" if isinstance(card, ControlCard) else "CF" if isinstance(card, FinalizationCard) else "CE"
        line(f"### Turno {state.turn} — {icon} {card_type}: {card.name}")
        if isinstance(card, ControlCard):
            line(
                f"- 🟩 Robo: CC **{card.name}**. "
                f"Mano ({_hand_indicator(state)}): {_hand_text(state)}."
            )
            if len(state.hand) > state.rules.max_control_hand_size:
                assessments = {item.definition_id: item for item in ai.assess_hand(state)}
                discarded_id = ai.choose_control_discard(state)
                assessment = assessments[discarded_id]
                engine.discard_control_from_hand(state, discarded_id)
                line(
                    f"- 🟩 Límite de mano: se descarta **{assessment.name}** "
                    f"(copias: {assessment.copies_in_hand}; comparaciones utilizables: "
                    f"{assessment.usable_comparisons}; valor: {assessment.best_effect_value})."
                )
            last_red_card_summary = audit_red_cards()
            turn_summary(last_red_card_summary)
            audit_events()
            continue

        if isinstance(card, FinalizationCard):
            line(
                f"- 🟧 Robo: CF **{card.name}**. "
                f"Mano antes de decidir ({_hand_indicator(state)}): {_hand_text(state)}."
            )
            plan = ai.choose_control_plan(state, card)
            finalization_bonus_parts = (
                [state.pending_cf_bonus] if state.pending_cf_bonus else []
            )
            if not plan.plays:
                line("- IA: no gasta CC; no puede mejorar la CF de forma rentable.")
            for position, play in enumerate(plan.plays, 1):
                held = next(item for item in state.hand if item.card.definition_id == play.card_definition_id)
                control = held.card
                assert isinstance(control, ControlCard)
                option = control.option(play.option_key)
                comparison = (
                    f" Comparación: {_comparison_text(state, option.comparison, state.pending_cc_bonus)}; superada."
                    if option.comparison is not None
                    else ""
                )
                line(f"- 🟩 CC {position}: **{control.name} — {option.label}**: {_effect_text(option.effect)}.{comparison}")
                engine.apply_control_play(state, play)
                if option.effect.cf_bonus:
                    finalization_bonus_parts.append(option.effect.cf_bonus)
            preview = engine.evaluate_finalization(state, card)
            _write_finalization_options(
                output, state, card, preview.outcome, finalization_bonus_parts
            )
            engine.resolve_finalization(state, instance, ai)
            line(f"- 🟧 CF aplicada: **{preview.resolution.outcome_name}** (nivel {preview.resolution.tier}).")
            last_red_card_summary = audit_red_cards()
            turn_summary(last_red_card_summary)
            audit_events()
            continue

        assert isinstance(card, EventCard)
        option = ai.choose_event_option(state, card)
        line(f"- 🟪 Robo: CE **{card.name}**.")
        _write_event_options(output, card, option)
        line(f"- 🟪 IA elige **{option.label}**.")
        line("- Los robos o CF extra que active el evento se resuelven inmediatamente según el motor.")
        engine.resolve_event(state, instance, ai)
        last_red_card_summary = audit_red_cards()
        turn_summary(last_red_card_summary)
        audit_events()

    line()
    line("## Resultado final")
    line()
    result_icon = "🏆" if state.player_goals > state.bot_goals else "💔" if state.bot_goals > state.player_goals else "🤝"
    line(f"### {result_icon} Marcador final: Jugador {state.player_goals} – {state.bot_goals} Bot")
    line()
    line("| Métrica | Resultado |")
    line("| --- | ---: |")
    line(f"| Goles del jugador | **{state.player_goals}** |")
    line(f"| Goles del bot por presión | **{state.bot_goals_from_pressure}** |")
    line(f"| Goles del bot por CR | **{state.bot_goals_from_red_cards}** |")
    line(f"| 🟨 Amarillas al rival | **{state.yellow_cards}** |")
    line(f"| 🟥 Rojas al rival | **{state.red_cards}** |")
    line(f"| 🟨 Amarillas propias | **{state.player_yellow_cards}** |")
    line(f"| 🟥 Rojas propias | **{state.player_red_cards}** |")
    line(f"| CR robadas | **{state.cr_draws}** |")
    line(f"| Presión final | **{state.pressure}** |")
    line(f"| CE resueltas | **{len(state.events_resolved)}** |")
    line(f"| CF resueltas | **{len(state.finalizations)}** |")
    line(f"| CC finales en mano | **{len(state.hand)}** |")
    line(f"| Sustituciones por lesión | **{state.injury_substitutions}** |")


def main() -> None:
    parser = argparse.ArgumentParser(description="Informe paso a paso de BG FÚTBOL")
    parser.add_argument("--seed", type=int, default=20260829)
    parser.add_argument(
        "--strategy",
        choices=("standard", "one_nil_low_cr"),
        default="standard",
    )
    parser.add_argument(
        "--player",
        type=int,
        nargs=3,
        metavar=("DEF", "MED", "AT"),
        default=(15, 15, 15),
        help="Atributos del jugador: DEF MED AT.",
    )
    parser.add_argument(
        "--bot",
        type=int,
        nargs=3,
        metavar=("DEF", "MED", "AT"),
        default=(15, 15, 15),
        help="Atributos del bot: DEF MED AT.",
    )
    parser.add_argument("--output", type=Path, help="Archivo Markdown de salida.")
    args = parser.parse_args()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", encoding="utf-8", newline="\n") as stream:
            write_match_trace(
                args.seed,
                stream,
                strategy=args.strategy,
                player=Team(*args.player),
                opponent=Team(*args.bot),
            )
        return
    import sys

    write_match_trace(
        args.seed,
        sys.stdout,
        strategy=args.strategy,
        player=Team(*args.player),
        opponent=Team(*args.bot),
    )


if __name__ == "__main__":
    main()
