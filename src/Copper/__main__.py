import asyncio 

from Server import server

async def main():
    print("Hello, World")
    await server('0.0.0.0', '8080')

asyncio.run(main())
