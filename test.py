import sys, requests, os, time
from funciones import sql

import concurrent.futures
from dotenv import load_dotenv

load_dotenv('private/.env')

api_key = os.getenv('API_KEY')
url = os.getenv('url')


session = requests.Session()

def crear_concurr_cursos(params):
    response = session.post(f"{url}", params=params).json()
    return response

def lista_concurr_cursos(resultados):
    try:
        list_params = [
        {
            "wstoken": api_key,
            "moodlewsrestformat": "json",
            "wsfunction": "core_course_create_categories",
            "courses[0][fullname]": resultado[0],
            "courses[0][shortname]": resultado[1],
            "courses[0][categoryid]": resultado[2],
            "courses[0][format]": 'weeks'
        } for resultado in resultados]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            responses = list(executor.map(crear_concurr_cursos, list_params))

        return responses
    
    except Exception as e:
        return f'Fallaste {e}'


lista_concurr_cursos()
