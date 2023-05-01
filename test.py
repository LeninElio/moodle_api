from concurrent.futures import ThreadPoolExecutor
import requests
from funciones import decorador, moodle, sql


@decorador.calcular_tiempo
def desmatricular_usuarios():
    """
    Esta función recupera una lista de usuarios inscritos, intenta cancelar su inscripción al mismo
    tiempo mediante una API de Moodle y devuelve los errores encontrados durante el proceso.

    :return: ya sea las respuestas de las llamadas desmatricular_usuario concurrentes o un error 
    si hay una excepción de solicitudes.
    """
    query = '''EXEC le_matriculados '2020-1', '161.0704.574' '''
    resultados = sql.lista_query(query)

    try:
        if resultados != []:
            list_params = moodle.concurr_desmatricular_usuario(resultados)

            with ThreadPoolExecutor() as executor:
                responses = list(executor.map(moodle.creacion_concurrente, list_params))

            return responses

    except requests.exceptions.RequestException as error:
        return error


@decorador.calcular_tiempo_arg
def desmatricular_usuario_username(username):
    """
    Esta función da de baja a un usuario de sus cursos en Moodle utilizando su nombre de usuario.
    
    :param username: El nombre de usuario del estudiante que necesita ser dado de baja de sus cursos
    
    :return: ya sea una cadena "Creo que no existe ese alumno" si el alumno no existe en la base de
    datos, o una lista de respuestas de un proceso simultáneo de cancelación de la inscripción del
    alumno en sus cursos en Moodle. Si hay un error con las solicitudes realizadas durante el 
    proceso concurrente, la función devolverá el mensaje de error.
    """
    query = f'''SELECT moodle_id FROM dbo.Alumno WHERE Alumno='{username}' '''
    alumno = sql.lista_query_uno(query)

    if alumno is None:
        return 'Creo no existe ese alumno'

    cursos = alumno
    cursos = [(curso, alumno) for curso in cursos]

    try:
        if cursos != []:

            list_params = moodle.concurr_desmatricular_usuario(cursos)

            with ThreadPoolExecutor() as executor:
                responses = list(executor.map(moodle.creacion_concurrente, list_params))

            return responses

    except requests.exceptions.RequestException as error:
        return error


@decorador.calcular_tiempo
def obtener_matriculas_moodle():
    """
    Esta función obtiene ID de cursos de Moodle y realiza solicitudes simultáneas para crear cursos.
    
    :return: ya sea una lista de respuestas de una solicitud de API de Moodle o una cadena 
    que indica que no hay cursos o un error probable.
    """
    # query = "SELECT top 3 lc.id_moodle from sva.le_cursos lc"
    # cursos = sql.lista_query_especifico(query)
    cursos = [439]

    try:
        if cursos:
            list_params = moodle.async_peticion_por_idcurso(cursos)

            with ThreadPoolExecutor() as executor:
                responses = list(executor.map(moodle.creacion_concurrente, list_params))

            return responses

    except requests.exceptions.RequestException as re_ex:
        return f'Probable error, {re_ex}'


obtener = obtener_matriculas_moodle()
print(obtener)
