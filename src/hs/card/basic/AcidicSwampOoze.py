from hs.card.card import Card, CardType, CardSet, Keyword
from hs.event.output.lost_weapon_event import LostWeaponEvent


class AcidicSwampOoze(Card):

    def __init__(self):
        super().__init__(1, "Acidic Swamp Ooze", 2, CardType.minion, CardSet.basic, [Keyword.battlecry], "neutral")

    def battlecry(self, board, position, your, opponent):
        if opponent in board:
            del board.weapon[opponent]
            return LostWeaponEvent(opponent)


Card.register(AcidicSwampOoze())
