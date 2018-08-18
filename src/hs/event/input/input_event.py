from abc import ABC
from hs.event.EventException import EventException


class InputEvent(ABC):

    event_types = {}

    @classmethod
    def register(cls, name, t):
        cls.event_types[name] = t

    @classmethod
    def input_handler(cls, event: str, data: dict):
        if event in cls.event_types:
            return cls.event_types[event](data)
        else:
            raise EventException("invalid event type: " + event)
