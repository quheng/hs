from hs.event.input.input_event import InputEvent

class OverEvent(InputEvent):

    name = "over"


InputEvent.register(OverEvent.name, OverEvent)
