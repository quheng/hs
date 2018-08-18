from hs.event.EventException import EventException
from hs.event.input.input_event import InputEvent

class AttackEvent(InputEvent):

    name = "attack"

    def __init__(self, data: dict):
        if "our" not in data:
            raise EventException("missing our field")
        if "enemy" not in data:
            raise EventException("missing enemy field")
        self.our = data["our"]
        self.enemy = data["enemy"]


InputEvent.register(AttackEvent.name, AttackEvent)
