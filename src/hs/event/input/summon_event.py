from hs.event.EventException import EventException
from hs.event.input.input_event import InputEvent


class SummonEvent(InputEvent):

    name = "summon"

    def __init__(self, data: dict):
        if "hand" not in data:
            raise EventException("missing hand field")
        if "battlefield" not in data:
            raise EventException("missing battlefield field")
        self.hand = data["hand"]
        self.battlefield = data["battlefield"]


InputEvent.register(SummonEvent.name, SummonEvent)
