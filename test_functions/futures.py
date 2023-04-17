import sys, requests, os, time
sys.path.append(".")
from funciones import sql

import concurrent.futures
from dotenv import load_dotenv

load_dotenv('private/.env')

api_key = os.getenv('API_KEY')
url = os.getenv('url')

resultados = [('01', 'I   ', 921, '2020-5-02-01-I   ')]

session = requests.Session()

def crear_sub_categoria(params):
    response = session.post(f"{url}", params=params).json()
    return response

def crear_cat_ciclos():
    try:
        list_params = [
        {
            "wstoken": api_key,
            "moodlewsrestformat": "json",
            "wsfunction": "core_course_create_categories",
            "categories[0][name]": resultado[1],
            "categories[0][idnumber]": resultado[3],
            "categories[0][description]": resultado[1],
            "categories[0][parent]": resultado[2]
        } for resultado in resultados]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            responses = list(executor.map(crear_sub_categoria, list_params))

        for response in responses:
            data = {'numeracion': response[0]['name'], 'parent': response[0]['id']}
            sql.insertar_datos('sva.le_ciclo', data)
    
    except Exception as e:
        return f'Fallaste {e}'


inicio = time.time()
crear_cat_ciclos()
fin = time.time()

print(f"Tiempo de ejecución: {fin - inicio} segundos")