from funciones import moodle, sql, funciones
from concurrent.futures import ThreadPoolExecutor 
import pandas as pd


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


# funcion que permite obtener a los alumnos y sus cursos matriculados a partir de un id curso
# para muchos datos no es optimo
@funciones.calcular_tiempo
def obtener_matriculas_moodle():
    # query = "SELECT top 3 lc.id_moodle from sva.le_cursos lc"
    
    # cursos = sql.lista_query_especifico(query)
    cursos = [439]

    try:
        if cursos != []:

            list_params = moodle.async_peticion_por_idcurso(cursos)
            
            with ThreadPoolExecutor() as executor:
                responses = list(executor.map(moodle.creacion_concurrente, list_params))

            matriculas = [(cursos['id'], matriculados['id']) for resultado in responses for matriculados in resultado for cursos in matriculados['enrolledcourses']]

            # insertar_matriculas_bd(matriculas)
            print(matriculas)

        else:
            print('No hay cursos')

    except Exception as e:
            return e


# obtener_matriculas_moodle()
# desmatricular_usuarios()(
# desmatricular_usuario_username('161.0704.54')('131.2502.153')

# def mifuncion(param):
#     print(param)
#     return mifuncion


# mifuncion('A')('B')



@funciones.calcular_tiempo_arg
def ocultar_cursos_moodle(semestre, lista = False):
    # Lista es un valor booleano para saber que el primer parametro que se esta enviando es una lista
    if lista and not isinstance(semestre, list):
        return print(f'{semestre} no es una lista valida.')

    if not lista:
        query = f"SELECT lc.id_moodle from sva.le_cursos lc WHERE lc.semestre = '{semestre}'"
        cursos = sql.lista_query_especifico(query)
    else: 
        cursos = semestre

    try:
        if cursos != []:

            list_params = moodle.ocultar_cursos(cursos)
            
            with ThreadPoolExecutor() as executor:
                executor.map(moodle.creacion_concurrente, list_params)

            return 'Cursos ocultados correctamente.'

        else:
            return 'No hay mas cursos por ocultar.'

    except Exception as e:
            return f'Error al finalizar el semestre, error: {e}'


# listax = [2, 10, 3, 6, 7]

# ocultar = ocultar_cursos_moodle('2020-1')
# print(ocultar)


@funciones.calcular_tiempo_arg
def obtener_visibilidad_curso(semestre):
    query = f"SELECT lc.id_moodle from sva.le_cursos lc WHERE lc.semestre = '{semestre}'"
    
    cursos = sql.lista_query_especifico(query)
    try:
        if cursos != []:

            list_params = moodle.listar_cursos_por_idcurso(cursos)
            
            with ThreadPoolExecutor() as executor:
                respuestas = list(executor.map(moodle.creacion_concurrente, list_params))
 
            # ocultos = [respuesta['courses'][0]['id'] for respuesta in respuestas if respuesta['courses'] != [] if respuesta['courses'][0]['visible'] == 0]
            
            visibles = [respuesta['courses'][0]['id'] for respuesta in respuestas if respuesta['courses'] != [] if respuesta['courses'][0]['visible'] == 1]

            # print('Ocultos: ', ocultos)
            # print('Visibles: ', visibles)

            ocultar_cursos_moodle(visibles, True)
            
            return f'Cantidad de cursos que aun estan visibles: {len(visibles)}'

        else:
            return 'No hay mas cursos para procesar.'

    except Exception as e:
            return f'Error en la obtencion de la visibilidad de cursos, error {e}'


visibles = obtener_visibilidad_curso('2020-1')
print(visibles)
