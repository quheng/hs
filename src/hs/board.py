from enum import Enum
from hs.card.card import cards

class Timing(Enum):
    summon = "summon"
    play_card = "play_card"
    minion_died = "minion_died"


class Board:
    def __init__(self, users_deck):
        self.deck = {}
        for user, deck_index in users_deck.items():
            self.deck[user] = [cards[i] for i in user.get_deck(deck_index)]
        self.battle_field = {}
        self.hand = {}
        self.global_buff = []
        self.buff = {}
        self.grave = {}
        self.hero_health = {}
        self.weapon = {}
        self.hero_attack = {}
        self.hero_armor = {}
