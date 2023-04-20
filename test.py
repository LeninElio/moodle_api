from funciones import moodle, sql, principal
import concurrent.futures
import pandas as pd

@principal.calcular_tiempo
def conwith():
    with open('./test_data/temp_data.txt', 'r', encoding='utf-8') as file:
        datos = file.readlines()
        # resultados = [[int(x) for x in dato.split(',')] for dato in datos]
    
    print(datos)
    # return resultados

conwith()
