import asyncio
import json
import logging
import websockets
from concurrent.futures import ThreadPoolExecutor

from hs.room import Room, RoomState, room_dict
from hs.event.input.input_event import InputEvent
from hs.event.EventException import EventException
from hs.user import User
from hs.game import Game

logging.basicConfig()

executor = ThreadPoolExecutor(max_workers=3)


async def join_room(user: User, current_room: Room, ws:websockets):
    await current_room.register(user, ws)
    if len(current_room.users) > 1:
        game = Game(current_room)
        current_room.start_game()
        loop = asyncio.get_event_loop()
        loop.run_in_executor(executor, game.game_loop)


async def hs(ws: websockets, path):
    user = User.login()
    await ws.send("id: " + user.id)
    current_room = room_dict.setdefault(path, Room(path))
    try:
        if current_room.state == RoomState.waiting:
            await join_room(user, current_room, ws)
        elif current_room.state == RoomState.gaming:
            # todo reconnect
            print("gaming")
            pass
        async for message in ws:
            await current_room.trigger_event(user, json.loads(message))
    finally:
        # todo reconnect
        await current_room.unregister(user)
        current_room.clear()
        pass

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(
        websockets.serve(hs, 'localhost', 6789))
    asyncio.get_event_loop().run_forever()
