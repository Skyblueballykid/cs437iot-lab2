#!/usr/bin/env python

# https://pypi.org/project/websockets/ example client
import asyncio
from websockets import connect

async def hello(uri):
    async with connect(uri) as websocket:
        await websocket.send("Hello world!")
        await websocket.recv()

asyncio.run(hello("ws://localhost:8765"))