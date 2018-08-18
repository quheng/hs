from hs.event.output.output_event import OutputEvent


class DrawCardEvent(OutputEvent):
    name = "lost_weapon"

    __slots__ = ["user_id", "card_id"]

    def __init__(self, user_id, card_id):
        self.user_id = user_id
        self.card_id = card_id
