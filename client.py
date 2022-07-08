import aiohttp
import asyncio

import random

from typing import Dict, Any


def request_randomizer() -> Dict[str, Any]:
    piece = random.choice(["rook", "bishop", "knight", "queen"])
    size = random.randint(1, 6)  # Its too slow for 7 and 8

    return {"n": str(size), "chessPiece": piece}


async def get_response(session, json):
    print("#######################################")
    print("Requesting: ", json)
    async with session.get('http://localhost:8088', json=json) as resp:
        print("Status: ", resp.status)
        print("Response: ", await resp.json())
    print("#######################################")


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [get_response(session, request_randomizer()) for i in range(10)]
        await asyncio.gather(*tasks)

asyncio.run(main())
