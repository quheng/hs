from hs.event.output.output_event import OutputEvent


class LostWeaponEvent(OutputEvent):
    __slots__ = ["user_id"]
    name = "lost_weapon"

    def __init__(self, user_id):
        self.user_id = user_id
