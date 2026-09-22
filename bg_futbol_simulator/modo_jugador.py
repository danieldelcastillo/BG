
"""BG FÚTBOL - Modo jugador humano v2.

Interfaz manual sobre el motor existente.
"""
from __future__ import annotations

import random

from .cards import ControlCard, FinalizationCard, EventCard
from .engine import RulesEngine
from .game_state import Team


def print_state(state):
    print("\n" + "="*70)
    print(f"TURNO {state.turn}")
    print(f"MARCADOR: Jugador {state.player_goals} - {state.bot_goals_from_pressure + state.bot_goals_from_red_cards} Bot")
    print(f"Presión: {state.pressure}")
    print("="*70)


def print_hand(state):
    print("\nTU MANO CC")
    print("-"*70)
    if not state.hand:
        print("(sin cartas)")
        return

    for i, instance in enumerate(state.hand, 1):
        card = instance.card
        print(f"\n{i}) {card.name}")
        if isinstance(card, ControlCard):
            for j, option in enumerate(card.options, 1):
                print(f"   {j}. {option.label}")
                print(f"      CC {option.effect.cc_bonus:+} | CF {option.effect.cf_bonus:+} | Presión {option.effect.pressure_delta:+}")


def choose_card(state):
    cards = [c for c in state.hand if isinstance(c.card, ControlCard)]
    if not cards:
        return None

    while True:
        print("\nElegir CC:")
        for i,c in enumerate(cards,1):
            print(f"{i}. {c.card.name}")
        print("0. Pasar a CF")

        x=input("> ").strip()
        if x=="0":
            return None
        if x.isdigit() and 1 <= int(x) <= len(cards):
            return cards[int(x)-1]


def human_match():
    engine=RulesEngine()
    state=engine.create_match_state(
        Team(15,15,15),
        Team(15,15,15),
        random.Random(),
    )

    print("BG FÚTBOL - MODO JUGADOR v2")

    while not state.finished:
        print_state(state)
        print_hand(state)

        card=choose_card(state)
        if card:
            print(f"\nHas seleccionado: {card.card.name}")
            for i,opt in enumerate(card.card.options,1):
                print(f"{i}. {opt.label}")
            input("Selecciona opción y pulsa ENTER (motor conectado en siguiente integración)")

        input("\nENTER para continuar...")

if __name__=="__main__":
    human_match()
