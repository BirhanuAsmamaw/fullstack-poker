import random

def card_formatter(cards) -> str:
    card_str = str(cards)

    board = ''
    for i in card_str:
        if i != ',' and i != ' ' and i != '(' and i != ')':
            board += i
    
    return board

def generate_unique_hole_cards(num_players: int = 6) -> list[str]:
    """
    Generates unique hole cards for each player.
    Args:
        num_players (int): The number of players in the game.
    Returns:
        list[str]: A list of unique hole cards for each player.
    """

    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    suits = ['c', 'd', 'h', 's']
    full_deck = [rank + suit for rank in ranks for suit in suits]
    print(f"full_deck: {full_deck}")
    random.shuffle(full_deck)

    hole_cards = []
    for _ in range(num_players):
        card1 = full_deck.pop()
        card2 = full_deck.pop()
        hole_cards.append(card1 + card2)
    
    print("hh", hole_cards)
    return hole_cards