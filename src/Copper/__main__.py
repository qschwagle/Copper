import asyncio 

from Server import server

async def main():
    print("Hello, World")
    await server()

asyncio.run(main())
