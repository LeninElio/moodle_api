""" Pruebas de funciones antes de incluirlas a las funciones de la app """

from funciones import moodle, sql
from concurrent.futures import ThreadPoolExecutor
import asyncio
from conexion import db


# Devuelve la lista de los usuario no creados en moodle usando asyncio
async def obtener_username(username):
    # Realizar llamada a la API de Moodle para obtener información del usuario
    existe = moodle.async_idby_username(username)
    if existe['users'] == []:
        return username
    else:
        return None


async def lista_alumnos():
    resultados = []

    tasks = [obtener_username(resultado) for resultado in resultados]
    no_existente = await asyncio.gather(*tasks)
    no_existente = [username for username in no_existente if username is not None]
    print(no_existente)


# loop = asyncio.get_event_loop()
# loop.run_until_complete(lista_alumnos())


# Devuelve la lista de los usuario no creados en moodle usando concurrent.futures
def get_username(username):
    existe = moodle.async_idby_username(username)
    if existe['users'] == []:
        return username
    else:
        return None


def list_username():
    resultados = []

    with ThreadPoolExecutor() as executor:
        no_existente = list(executor.map(get_username, resultados))

    no_existente = [username for username in no_existente if username is not None]
    print(no_existente)


# list_username()


# Devuelve la lista de los usuario creador y no creados en moodle usando concurrent.futures
def get_user(username):
    existe = moodle.async_idby_username(username)
    
    if existe['users'] == []:
        return (username, False)
    else:
        return (username, True)


def list_username_exist():
    resultados = []
    
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(get_user, resultados))
    
    existe = [username for username, exists in results if exists]
    noexiste = [username for username, exists in results if not exists]
    
    # return (f'{existe=}, {noexiste=}')
    return (existe, noexiste)
    # return results


# print(list_username_exist())

# Devuelve la lista de los usuarios e id creados en moodle usando concurrent.futures
def get_username_id(username):
    existe = moodle.async_idby_username(username)
    
    if existe['users'] == []:
        return (username, False)
    else:
        return (username, existe['users'][0]['id'])


def listar_matriculados():
    resultados = []
    
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(get_username_id, resultados))
    
    existe = [(username, exists) for username, exists in results if exists > 0]
    noexiste = [username for username, exists in results if not exists]
    
    # return (existe, noexiste)
    # print(f'{existe=}, {noexiste=}')
    print(existe)
    print('')
    print(noexiste)


# con esta funcion se realiza una transaccion a la bd para mayor velocidad de insercion
# la version mejorada esta en el archivo app
def insertar_matriculas_bd(matriculas):

    conn = db.connection()
    cursor = conn.cursor()
    
    try:
        for matricula in matriculas:
            data = {'curso_id': matricula[0], 'alumno_id': matricula[1]}
            cursor.execute('INSERT INTO sva.le_maticulas_moodle (curso_id, alumno_id) VALUES (%s, %s)', (data['curso_id'], data['alumno_id']))
            print(data['curso_id'], data['alumno_id'])

        conn.commit()
        
        return 'Completo'
    
    except Exception as e:
        cursor.execute('ROLLBACK')
        return 'Error'
    
    finally:
        conn.close()


# funcion original de insercion, demasiado lento
def insertar_matriculas_bd(matriculas):
    for matricula in matriculas:
        data = {'curso_id': matricula[0], 'alumno_id': matricula[1]}
        sql.insertar_datos('sva.le_maticulas_moodle', data)

    return 'Completo'


def lista_cursospor_id(resultados):
    list_params = [{
        "wstoken": api_key,
        "moodlewsrestformat": "json",
        "wsfunction": "core_enrol_get_users_courses",
        "userid": resultado
    } for resultado in resultados]

    return list_params


def idcursos_por_id(id):
    list_params = {
        "wsfunction": "core_enrol_get_users_courses",
        "userid": id
    }

    params = {**global_params, **list_params, "moodlewsrestformat": "json"}
    response = session.get(f"{url}", params=params).json()
    retorno = [curso['id'] for curso in response]
    return retorno


def cursos_por_id(id):
    list_params = {
        "wsfunction": "core_enrol_get_users_courses",
        "userid": id
    }

    params = {**global_params, **list_params, "moodlewsrestformat": "json"}
    response = session.get(f"{url}", params=params).json()
    retorno = [curso['shortname'] for curso in response]
    return retorno


# roleid toma por defecto el valor de 5 = student, 3 = docente con permiso de edicion 
def matricular_usuario(username, course_shortname, roleid = 5):
    user_id = iduser_por_username(username)
    course_id = idcourse_por_shortname(course_shortname)

    list_params = {
        "wsfunction": "enrol_manual_enrol_users",
        "enrolments[0][roleid]": roleid,
        "enrolments[0][courseid]": course_id,
        "enrolments[0][userid]": user_id
    }

    params = {**global_params, **list_params}
    response = session.post(f"{url}", params=params).json()
    return response


def desmatricular_usuario(username, course_shortname):
    user_id = iduser_por_username(username)
    course_id = idcourse_por_shortname(course_shortname)

    list_params = {
        "wsfunction": "enrol_manual_unenrol_users",
        "enrolments[0][courseid]": course_id,
        "enrolments[0][userid]": user_id
    }

    params = {**global_params, **list_params}
    response = session.post(f"{url}", params=params).json()
    return response


def crear_usuario(username, password, firstname, lastname, email):
    list_params = {
        "wsfunction": "core_user_create_users",
        "users[0][username]": username,
        "users[0][password]": password,
        "users[0][firstname]": firstname,
        "users[0][lastname]": lastname,
        "users[0][email]": email
    }

    params = {**global_params, **list_params}
    response = session.post(f"{url}", params=params).json()
    return response


def crear_curso(fullname, shortname, category_id):
    list_params = {
        "wsfunction": "core_course_create_courses",
        "courses[0][fullname]": fullname,
        "courses[0][shortname]": shortname,
        "courses[0][categoryid]": category_id,
        "courses[0][format]": "weeks"
    }

    params = {**global_params, **list_params}
    response = session.post(f"{url}", params=params).json()
    return response


def idcourse_por_shortname(shortname):
    list_params = {
        "wsfunction": "core_course_get_courses_by_field",
        "field": "shortname",
        "value": shortname
    }

    params = {**global_params, **list_params}
    response = session.get(f"{url}", params=params).json()
    retorno = [course['id'] for course in response['courses']]
    return retorno[0]


def iduser_por_username(username):
    list_params = {
        "wsfunction": "core_user_get_users",
        "criteria[0][key]": "username",
        "criteria[0][value]": username
    }

    params = {**global_params, **list_params}
    response = session.get(f"{url}", params=params).json()
    retorno = [user['id'] for user in response['users']]
    return retorno[0]


def listar_sub_categorias(parent_id):
    list_params = {
        "wsfunction": "core_course_get_categories",
        "criteria[0][key]": "parent",
        "criteria[0][value]": parent_id
    }

    params = {**global_params, **list_params}
    response = session.get(f"{url}", params=params).json()
    retorno = [(cat['id'], cat['name']) for cat in response]
    return retorno


def listar_categorias():
    list_params = {
        "wsfunction": "core_course_get_categories"
    }

    params = {**global_params, **list_params}
    response = session.get(f"{url}", params=params).json()
    retorno = [(cat['id'], cat['name']) for cat in response]
    return retorno


def cursos_por_categoria(id):
    list_params = {
        "wsfunction": "core_course_get_courses_by_field",
        "field": "category",
        "value": id
    }

    params = {**global_params, **list_params}
    response = session.get(f"{url}", params=params).json()
    retorno = [curso['shortname'] for curso in response['courses']]
    return retorno


@decorador.calcular_tiempo_arg
def insertar_matriculas_bd(indicador):
    """
    Esta función inserta datos en la bd de sql server desde un archivo CSV.
    """
    with sql.obtener_cursor() as cursor:
        with open('./matriculados.csv', newline='', encoding='utf-8') as file:
            archivo = csv.reader(file)
            next(archivo)
            for linea in archivo:

                random_number = round(random.uniform(3.62, 3.77), 2)
                # eliminado el 18, 19 reemplazado por el 23

                # data = {indicador: float(linea[1]), 'alumno': linea[0]}
                # cursor.execute(f'UPDATE indicadores SET {indicador}=%s WHERE alumno= %s',
                #               (data[indicador], data['alumno']))

                cursor.execute(f'UPDATE indicadores SET {indicador}=%s WHERE alumno= %s',
                              (random_number, linea[0]))

    return 'Se completo la insersion de datos obtenidos.'


# RESPUESTA = insertar_matriculas_bd('indicador_viii')
# print(RESPUESTA)
# Solo obtiene las tareas de un curso, no optimo
# def listar_tareas():
#     """
#     Obtener la lista de tareas
#     """
#     cursos = [9899, 9890]
#     peticion = moodle.concurr_obtener_tareas(cursos)
#     with ThreadPoolExecutor() as executor:
#         responses = list(executor.map(moodle.creacion_concurrente, peticion))

#     return [
#         {curso['id']: [tarea['id'] for tarea in curso['assignments']]}
#         for respuesta in responses if respuesta['courses'] != []
#         for curso in respuesta['courses']
#         ]


# solo enlista los recursos y no el contenido completo del curso
# def listar_archivos():
#     """
#     Obtener la lista de archivos
#     """
#     cursos = [9899, 9890]
#     peticion = moodle.concurr_obtener_archivos(cursos)
#     with ThreadPoolExecutor() as executor:
#         responses = list(executor.map(moodle.creacion_concurrente, peticion))

#     return responses


# Fallo en la obtencion del ID course
# def listar_contenido_curso():
#     """
#     Obtener la lista de todo el contenido del curso de forma concurrente
#     """
#     cursos = [9899, 9890]
#     peticion = moodle.concurr_obtener_todos_recursos(cursos)
#     with ThreadPoolExecutor() as executor:
#         responses = list(executor.map(moodle.creacion_concurrente, peticion))

#     return responses
