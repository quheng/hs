from hs.event.EventException import EventException
from hs.event.input.input_event import InputEvent


class ChooseDeckEvent(InputEvent):

    name = "choose_deck"

    def __init__(self, data: dict):
        if "deck_index" not in data:
            raise EventException("missing deck_index field")
        self.deck_index = data["deck_index"]


InputEvent.register(ChooseDeckEvent.name, ChooseDeckEvent)
