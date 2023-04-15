import aiohttp
import asyncio
import async_timeout


async def obtener_nombre(session, url, personaje):
    async with async_timeout.timeout(10):
        async with session.get(url.format(personaje)) as response:
            data = await response.json()
            return data['name']


async def main():
    url = 'https://rickandmortyapi.com/api/character/{}'
    tareas = []
    async with aiohttp.ClientSession() as session:
        for personaje in range(1, 10):
            tarea = asyncio.ensure_future(obtener_nombre(session, url, personaje))
            tareas.append(tarea)
        nombres = await asyncio.gather(*tareas)
        print(nombres)


if __name__ == '__main__':
    asyncio.run(main())
