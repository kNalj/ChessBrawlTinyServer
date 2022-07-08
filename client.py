import aiohttp
import asyncio


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8088', json={"n": "4", "chessPiece": "queen"}) as resp:
            print("Status: ", resp.status)
            print("Response: ", await resp.json())

asyncio.run(main())
