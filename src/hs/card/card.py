from abc import ABC
from enum import Enum
import json
import os
from os.path import dirname, basename, isfile, join
import glob
import importlib

cards = list(range(1500))


class CardType(Enum):
    minion = "minion"
    weapon = "weapon"
    spell = "spell"


class Rarity(Enum):
    free = "free"
    common = "common"
    rare = "rare"
    epic = "epic"
    legendary = "legendary"


class Race(Enum):
    beast = "beast"
    demon = "demon"
    dragon = "dragon"
    elemental = "elemental"
    mech = "mech"
    murloc = "murloc"
    pirate = "pirate"
    totem = "totem"


class CardSet(Enum):
    basic = "basic"
    classic = "classic"


class Keyword(Enum):
    battlecry = "battlecry"


class CardClass(Enum):
    neutral = "neutral"
    shaman = "shaman"
    hunter = "hunter"
    mage = "mage"
    warrior = "warrior"
    rogue = "rogue"
    paladin = "paladin"
    druid = "druid"
    warlock = "warlock"
    priest = "priest"


class Card(ABC):

    @staticmethod
    def register(card):
        cards[card.index] = card

    def __init__(self, index, name, cost, card_type, card_set, keywords, card_class):
        self.index: int = index
        self.name: int = name
        self.cost: int = cost
        self.card_type: CardType = card_type
        self.card_set: CardSet = card_set
        self.keywords: [] = keywords
        self.hocks: callable = []
        self.card_class: CardClass = card_class


class Minion(Card):

    def __init__(self, data: dict):
        super().__init__(data["index"], data["name"], data["cost"], CardType.minion, data["set"], data.get("keywords", []), data["card_class"])
        self.attack = data["attack"]
        self.health = data["health"]


def load_card_from_json(card_set):
    file_name = os.path.join(dirname(__file__), card_set.value, "cards.json")
    with open(file_name, 'r') as fp:
        data = json.load(fp)
        for card_data in data:
            if card_data["type"] == CardType.minion.value:
                card_data["set"] = card_set
                Card.register(Minion(card_data))


def load_card_from_class(card_set):
    modules = glob.glob(join(dirname(__file__), card_set.value, "*.py"))
    for module_name in [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]:
        importlib.import_module("hs.card.basic." + module_name)

# import cards
import hs.card.basic
load_card_from_json(CardSet.basic)
load_card_from_class(CardSet.basic)


