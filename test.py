from funciones import moodle, sql, principal
import concurrent.futures
import pandas as pd

@principal.calcular_tiempo
def pandita():
    with open('./test_data/temp_data_copy.txt', 'r', encoding='utf-8') as archivo:
        datos_objeto = [eval(linea) for linea in archivo]

    for obj in datos_objeto:
        print(obj)
        # try:
        #     id = obj[0]['users'][0]['id']
        #     username = obj[0]['users'][0]['username']
        #     email = obj[0]['users'][0]['email']
        #     course_id = obj[1]['courses'][0]['id']
        #     fullname = obj[1]['courses'][0]['fullname']
        #     print(id, username, email, course_id, fullname)
        # except (KeyError, IndexError):
        #     print('Error: objeto no tiene la estructura esperada')
        #     continue



pandita()