from app.models import ManaPool, ManaCost


def is_card_playable(card_mana_cost: str, opponent_mana: ManaPool) -> bool:
    cost = ManaCost.from_string(card_mana_cost)
    return opponent_mana.can_pay(cost)


def enrich_cards_with_playability(cards: list[dict], opponent_mana: ManaPool) -> None:
    for card in cards:
        card["is_playable"] = is_card_playable(card.get("mana_cost", ""), opponent_mana)


def enrich_decks_with_playability(decks: list[dict], opponent_mana: ManaPool) -> None:
    for deck in decks:
        enrich_cards_with_playability(deck.get("cards", []), opponent_mana)