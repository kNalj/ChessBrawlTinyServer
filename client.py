import aiohttp
import asyncio


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8088') as resp:
            print("Status: ", resp.status)
            print("Response: ", await resp.text())

asyncio.run(main())
