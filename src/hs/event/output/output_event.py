import json


class OutputEvent:
    def __str__(self):
        return json.dumps(self.to_json())

    def to_json(self):
        return {slot: getattr(self, slot) for slot in self.__slots__}
