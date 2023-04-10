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