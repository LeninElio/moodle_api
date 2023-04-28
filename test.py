from funciones import moodle, sql, funciones
from concurrent.futures import ThreadPoolExecutor 
import pandas as pd

@funciones.calcular_tiempo
def matricular_usuarios():
    query = f''' EXEC le_matriculados '2020-1' '''
    # query = f''' EXEC le_matriculados '2020-1', '161.0704.574' '''
    
    resultados = sql.lista_query(query)

    try:
        if resultados != []:

            list_params = moodle.concurr_matricular_usuario(resultados)

            with ThreadPoolExecutor() as executor:
                responses = list(executor.map(moodle.creacion_concurrente, list_params))

            return responses
        else:
            print('No hay mas datos')

    except Exception as e:
            return e


@funciones.calcular_tiempo
def desmatricular_usuarios():
    query = f''' EXEC le_matriculados '2020-1', '161.0704.574' '''
    
    resultados = sql.lista_query(query)

    try:
        if resultados != []:

            list_params = moodle.concurr_desmatricular_usuario(resultados)

            with ThreadPoolExecutor() as executor:
                responses = list(executor.map(moodle.creacion_concurrente, list_params))

            return responses
        else:
            print('No hay datos')

    except Exception as e:
            return e


@funciones.calcular_tiempo_arg
def desmatricular_usuario_username(username):
    query = f'''SELECT moodle_id FROM dbo.Alumno WHERE Alumno='{username}' '''
    
    alumno = sql.lista_query_uno(query)

    if alumno is None:
         return print('Creo no existe ese alumno')

    cursos = moodle.idcursos_por_id(alumno)
    cursos = [(curso, alumno) for curso in cursos]

    try:
        if cursos != []:

            list_params = moodle.concurr_desmatricular_usuario(cursos)

            with ThreadPoolExecutor() as executor:
                responses = list(executor.map(moodle.creacion_concurrente, list_params))

            return responses

        else:
            print('No hay cursos')

    except Exception as e:
            return e


matricular_usuarios()
# desmatricular_usuarios()(
# desmatricular_usuario_username('161.0704.54')('131.2502.153')

# def mifuncion(param):
#     print(param)
#     return mifuncion


# mifuncion('A')('B')