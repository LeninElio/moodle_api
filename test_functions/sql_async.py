# import sys
# sys.path.append(".")
# from conexion import db
# from contextlib import contextmanager
# import time


# def lista_query(query):
#     conn = db.connection()
#     cursor = conn.cursor()
#     cursor.execute(query)
#     datos = cursor.fetchall()
#     return [dato for dato in datos]


# inicio = time.time()
# lista_query('select top 10000 * from dbo.Rendimiento')
# fin = time.time()

# print(f"Tiempo de ejecución: {fin - inicio} segundos")

import sys
sys.path.append(".")
import asyncio
import aioodbc
import time


conn_string = 'Driver={ODBC Driver 17 for SQL Server};Server=MSI;Database=Itunasam1404;Trusted_Connection=yes;'

async def lista_query(query):
    async with aioodbc.connect(dsn=conn_string) as conn:
        cursor = await conn.cursor()
        await cursor.execute(query)
        datos = await cursor.fetchall()
        return [dato for dato in datos]


async def main():
    inicio = time.time()
    await lista_query('select top 100 * from dbo.Rendimiento')
    fin = time.time()
    print(f"Tiempo de ejecución: {fin - inicio} segundos")

if __name__ == '__main__':
    asyncio.run(main())
