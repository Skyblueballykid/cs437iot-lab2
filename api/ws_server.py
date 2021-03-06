#!/usr/bin/env python
# https://pypi.org/project/websockets/

import asyncio
from websockets import serve

async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)

async def main():
    async with serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())
