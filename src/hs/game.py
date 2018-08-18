import json

from hs.board import Board
from hs.event.output.draw_card_event import DrawCardEvent
from hs.room import Msg, Room
from hs.event.input.over_event import OverEvent
from hs.event.input.choose_deck_event import ChooseDeckEvent
from hs.user import User


class Game:
    def __init__(self, room: Room):
        self.room = room
        self.board: Board = None
        self.current_user: User = None
        self.waiting_user: User = None

    def prepare_board(self):
        users_deck = {}
        while self.waiting_user is None:
            msg: Msg = self.room.event_queue.get()
            if msg.user in users_deck:
                self.room.send_msg_nowait(json.dumps({"status": -1, "msg": "please wait others to choose deck"}))
            else:
                if not isinstance(msg.event, ChooseDeckEvent):
                    self.room.send_msg_nowait(json.dumps({"status": -1, "msg": "please choose deck"}))
                else:
                    user = self.room.users[msg.user]
                    if self.current_user:
                        self.waiting_user = user
                    else:
                        self.current_user = user
                    users_deck[user] = msg.event.deck_index
                    self.room.send_msg_nowait(json.dumps({"status": 0, "msg": "got deck"}), user)

        self.board = Board(users_deck)

    def game_loop(self):
        self.room.send_msg_nowait(json.dumps({"status": 0, "msg": "choose your deck"}))
        self.prepare_board()
        self.room.send_msg_nowait(json.dumps({"status": 0, "msg": "game is start"}))
        # todo draw card
        while True:
            self.switch_user()
            print(self.board.deck, self.board.deck[self.current_user])
            card = self.board.deck[self.current_user].pop()
            self.room.send_msg_nowait(str(DrawCardEvent(self.current_user.id, card.index)), self.current_user)
            self.room.send_msg_nowait(str(DrawCardEvent(self.current_user.id, 0)), self.waiting_user)

            event = self.room.event_queue.get()
            if isinstance(event, OverEvent):
                exit(0)

    def switch_user(self):
        self.current_user, self.waiting_user = self.waiting_user, self.current_user
