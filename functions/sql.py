import pymssql
from dotenv import load_dotenv
import os

load_dotenv('private/.env')

server = os.getenv('server')
user = os.getenv('user')
password = os.getenv('password')
database = os.getenv('database')

def connection():
    conn = pymssql.connect(
        server=server,
        user=user,
        password=password,
        database=database
    )

    return conn

conn = connection()
cursor = conn.cursor()


def insertar_datos(table, data):
    columns = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
    cursor.execute(query, tuple(data.values()))
    conn.commit()


def lista_query(query):
    cursor.execute(query)
    datos = cursor.fetchall()
    return [dato for dato in datos]


def retorna_valores_semestre(tabla, semestre):
    cursor.execute(f"select id, parent from {tabla} where nombre = '{semestre}'")
    datos = cursor.fetchone()
    return datos

