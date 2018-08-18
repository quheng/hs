import random


class User:
    def __init__(self):
        self.card_group = []
        self.id = str(random.randrange(999999999))

    @staticmethod
    def login():
        return User()

    def get_deck(self, index):
        return [1, 1]
