from enum import Enum, auto
import json
import asyncio
import websockets
import queue

from hs.event.input.over_event import OverEvent
from hs.user import User
from hs.event.input.input_event import InputEvent
from hs.event.EventException import EventException


class RoomState(Enum):
    waiting = auto()
    gaming = auto()
    over = auto()  # not used now


class Msg:
    __slots__ = ["user", "event"]

    def __init__(self, user, event):
        self.event = event
        self.user = user


class Room:
    def __init__(self, room_number: str):
        self.users = {}
        self.state = RoomState.waiting
        self._ws = {}
        self.room_num = room_number
        self.event_queue: queue.Queue = None
        self.loop = None

    async def register(self, user: User, ws: websockets) -> (bool, dict):
        if len(self.users) > 1:
            await ws.send(json.dumps({'status': -1, "msg":"full room"}))
            # todo break connection
        else:
            self.users[user.id] = user
            self._ws[user.id] = ws
            await ws.send(json.dumps({'status': 0, 'msg':'welcome, ' + user.id + '!'}))

    async def unregister(self, user: User) -> (bool, dict):
        del self.users[user.id]
        del self._ws[user.id]
        if self.state == RoomState.waiting:
            return True, {'status': 0}
        elif self.state == RoomState.gaming:
            # todo reconnect
            await self.send_msg(json.dumps({'status': 0, 'msg': user.id + 'leave'}))
            pass
        else:
            pass

    def start_game(self):
        self.state = RoomState.gaming
        self.event_queue = queue.Queue()
        self.loop = asyncio.get_event_loop()

    def clear(self):
        self.state = RoomState.waiting

        self.event_queue.put(Msg(None, OverEvent()))
        self.event_queue = None

    def send_msg_nowait(self, msg, user=None):
        asyncio.run_coroutine_threadsafe(self.send_msg(msg, user), self.loop)

    async def send_msg(self, msg: str, user: User=None):
        if user is None:
            await asyncio.wait([ws.send(msg) for ws in self._ws.values()])
        else:
            await self._ws[user.id].send(msg)

    async def trigger_event(self, user: User, event: dict):
        if self.state != RoomState.gaming:
            await self.send_msg(json.dumps({'status': -1, "msg": "room is not ready"}), user)
        elif "event" in event:
            try:
                event: InputEvent = InputEvent.input_handler(event["event"], event)
                self.event_queue.put(Msg(user.id, event))
            except EventException as exce:
                await self.send_msg(json.dumps({'status': -1, "msg": exce.args[0]}), user)
        else:
            await self.send_msg(json.dumps({'status': -1, "msg": "invalid data format(missed event)"}), user)


room_dict = {}
