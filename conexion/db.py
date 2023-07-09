import os
import pymssql
from dotenv import load_dotenv

load_dotenv('private/.env')

server = os.getenv('server')
user = os.getenv('user')
password = os.getenv('password')
database = os.getenv('database')


def connection():
    """
    Conexión a la base de datos.
    """
    conn = pymssql.connect(
        server=server,
        user=user,
        password=password,
        database=database
        # trusted=True
    )

    return conn
