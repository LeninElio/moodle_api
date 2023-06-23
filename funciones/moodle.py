""" Este módulo contiene funciones que interactuan con la API de moodle """

import os
from collections import defaultdict
import requests
from dotenv import load_dotenv

load_dotenv('private/.env')

api_key = os.getenv('API_KEY')
url = os.getenv('url')


global_params = {
    "wstoken": api_key,
    "moodlewsrestformat": "json"
}


session = requests.Session()


def cursos_concurr_categoria(resultados):
    """
    Esta función toma una lista de resultados y devuelve una lista de parámetros para
    obtener cursos por categoría.

    :param resultados: Es una lista de tuplas que contienen los ID de categoría y sus nombres
    correspondientes.

    :return: una lista de diccionarios, donde cada diccionario contiene parámetros para para
    recuperar cursos que pertenecen a una categoría específica.
    """
    list_params = [{
        "wstoken": api_key,
        "moodlewsrestformat": "json",
        "wsfunction": "core_course_get_courses_by_field",
        "field": "category",
        "value": resultado[0]
    } for resultado in resultados]

    return list_params


def crear_categoria(cat_nombre, idnumber, cat_desc):
    """
    Esta función crea una nueva categoría en Moodle.

    :param cat_nombre: El nombre de la categoría que desea crear

    :param idnumber: El parámetro idnumber es un identificador único para la categoría.

    :param cat_desc: La descripción de la categoría que se está creando.

    :return: la respuesta de una solicitud POST realizada para crear una categoría en Moodle.
    """
    list_params = {
        "wsfunction": "core_course_create_categories",
        "categories[0][name]": cat_nombre,
        "categories[0][idnumber]": idnumber,
        "categories[0][description]": cat_desc,
    }

    params = {**global_params, **list_params}
    response = session.post(f"{url}", params=params).json()

    return response


def crear_sub_categoria(cat_nombre, idnumber, cat_desc, parent_id):
    """
    Esta función crea una subcategoría en Moodle utilizando los parámetros proporcionados.

    :param cat_nombre: El nombre de la subcategoría que desea crear
    :param idnumber: El parámetro idnumber es un identificador único para la categoría.

    :param cat_desc: cat_desc significa descripción de categoría.

    :param parent_id: El ID de la categoría principal bajo la cual se creará la subcategoría

    :return: la respuesta de una solicitud POST realizada para crear una subcategoría en Moodle.
    """
    list_params = {
        "wsfunction": "core_course_create_categories",
        "categories[0][name]": cat_nombre,
        "categories[0][idnumber]": idnumber,
        "categories[0][description]": cat_desc,
        "categories[0][parent]": parent_id
    }

    params = {**global_params, **list_params}
    response = session.post(f"{url}", params=params).json()

    return response


def creacion_concurrente(params):
    """
    Esta función envía una solicitud POST a una URL específica con parámetros dados y devuelve la
    respuesta en formato JSON.

    :param params: El parámetro "params" es un diccionario que contiene los datos que se
    enviarán en la solicitud HTTP POST.

    :return: La función `creacion_concurrente` está devolviendo una respuesta JSON.
    """
    response = session.post(f"{url}", params=params).json()
    return response


def lista_concurr_cursos(resultados):
    """
    La función toma una lista de información del curso y devuelve una lista de parámetros para crear
    esos cursos en Moodle usando la API de Moodle.

    :param resultados: Es una lista de tuplas que contienen información sobre los cursos a crear en
    Moodle.

    :return: una lista de diccionariospara crear un  curso utilizando la API de Moodle.
    """
    list_params = [
        {
            "wstoken": api_key,
            "moodlewsrestformat": "json",
            "wsfunction": "core_course_create_courses",
            "courses[0][fullname]": resultado[0],
            "courses[0][shortname]": resultado[1],
            "courses[0][categoryid]": resultado[2],
            "courses[0][idnumber]": resultado[4],
            "courses[0][format]": 'weeks',
            "courses[0][startdate]": resultado[3]
        } for resultado in resultados]

    return list_params


def lista_concurr_usuarios(resultados):
    """
    Esta función toma una lista de datos de usuario y crea una lista de diccionarios con los
    parámetros necesarios para crear esos usuarios usando la API de Moodle.

    :param resultados: Es una lista de listas que contiene la información de múltiples
    usuarios para ser creada en una plataforma Moodle.

    :return: una lista de diccionarios.
    """
    list_params = [{
        "wstoken": api_key,
        "moodlewsrestformat": "json",
        "wsfunction": "core_user_create_users",
        "users[0][username]": resultado[0],
        "users[0][password]": resultado[1],
        "users[0][firstname]": resultado[2],
        "users[0][lastname]": resultado[3],
        "users[0][email]": resultado[4]
    } for resultado in resultados]

    return list_params


def lista_concurr_byusername(resultados):
    """
    La función toma una lista de nombres de usuario y devuelve una lista de parámetros para una
    llamada a la API de Moodle para recuperar información del usuario.

    :param resultados: Es una lista de nombres de usuario para los que queremos recuperar
    información de usuario utilizando la API de Moodle. La función `lista_concurr_byusername`
    toma esta lista como entrada y devuelve una lista de diccionarios.

    :return: devuelve una lista de diccionarios para hacer una llamada a la API de Moodle para
    recuperar información del usuario en función de su nombre de usuario.
    """
    list_params = [{
        "wstoken": api_key,
        "moodlewsrestformat": "json",
        "wsfunction": "core_user_get_users",
        "criteria[0][key]": "username",
        "criteria[0][value]": resultado[0]
    } for resultado in resultados]

    return list_params


def lista_concurr_byusernamex(resultados):
    """
    La función toma una lista de nombres de usuario y devuelve una lista de parámetros para una
    llamada a la API de Moodle para recuperar información del usuario.

    :param resultados: Es una lista de nombres de usuario para los que queremos recuperar
    información de utilizando la API de Moodle.

    :return: una lista de diccionarios, para recuperar información sobre los usuarios con un
    nombre de usuario específico.
    """
    list_params = [{
        "wstoken": api_key,
        "moodlewsrestformat": "json",
        "wsfunction": "core_user_get_users",
        "criteria[0][key]": "username",
        "criteria[0][value]": resultado
    } for resultado in resultados]

    return list_params


def lista_concurr_byshortname(resultados):
    """
    Esta función toma una lista de resultados y devuelve una lista de parámetros para una
    llamada a la API de Moodle para obtener cursos por su nombre corto.

    :param resultados: Es una lista de tuplas que contienen el ID del curso y el nombre abreviado de
    cada curso

    :return: una lista de diccionarios para hacer una llamada a la
    API de Moodle para recuperar cursos por su campo de nombre abreviado.
    """
    list_params = [{
        "wstoken": api_key,
        "moodlewsrestformat": "json",
        "wsfunction": "core_course_get_courses_by_field",
        "field": "shortname",
        "value": resultado[1]
    } for resultado in resultados]

    return list_params


def lista_concurr_matriculas(resultados):
    """
    La función toma una lista de resultados y devuelve una lista de parámetros para inscribir a los
    usuarios en un curso.

    :param resultados: Es una lista de tuplas que contienen la ID de usuario y la ID del curso
    para cada inscripción que debe agregarse a un curso de Moodle.

    :return: una lista de diccionarios, donde cada diccionario contiene parámetros para inscribir
    a los usuarios en un curso en Moodle utilizando el método de inscripción manual.
    """
    list_params = [{
        "wstoken": api_key,
        "wsfunction": "enrol_manual_enrol_users",
        "enrolments[0][roleid]": 3,
        "enrolments[0][courseid]": resultado[1],
        "enrolments[0][userid]": resultado[0]
    } for resultado in resultados]

    return list_params


def async_idby_username(username):
    """
    Esta función toma un nombre de usuario como entrada y devuelve la ID de usuario
    mediante una llamada a la API de Moodle.

    :param username: El nombre de usuario del usuario para el que desea recuperar información.

    :return: La función `async_idby_username` devuelve una respuesta JSON. La respuesta contiene
    información sobre el usuario con el `nombre de usuario` dado, incluida su ID.
    """
    list_params = {
        "wsfunction": "core_user_get_users",
        "criteria[0][key]": "username",
        "criteria[0][value]": username
    }

    params = {**global_params, **list_params}
    response = session.get(f"{url}", params=params).json()
    return response


def async_idby_shortname(shortname):
    """
    Esta función recupera una lista de cursos función de un nombre abreviado determinado.

    :param shortname: El parámetro shortname es una cadena que representa el nombre corto
    de un curso. Esta función usa este parámetro para recuperar la ID del curso asociada
    con el nombre corto dado.

    :return: La función `async_idby_shortname` devuelve la respuesta en formato JSON.
    """
    list_params = {
        "wsfunction": "core_course_get_courses_by_field",
        "field": "shortname",
        "value": shortname
    }

    params = {**global_params, **list_params}
    response = session.get(f"{url}", params=params).json()
    return response


def async_peticion_por_idcurso(respuestas):
    """
    La función toma una lista de ID de cursos y devuelve una lista de parámetros para realizar
    solicitudes asincrónicas para recuperar usuarios inscritos para cada curso.

    :param respuestas: Una lista de ID de cursos para los que queremos recuperar usuarios inscritos

    :return: una lista de diccionarios.
    """
    list_params = [{
        "wstoken": api_key,
        "moodlewsrestformat": "json",
        "wsfunction": "core_enrol_get_enrolled_users",
        "courseid": respuesta
    } for respuesta in respuestas]

    return list_params


def concur_idby_username(resultados):
    """
    La función toma una lista de nombres de usuario y devuelve una lista de parámetros para una
    llamada a la API de Moodle para recuperar ID de usuario.

    :param resultados: Es una lista de nombres de usuario para los que queremos recuperar las ID de
    usuario.

    :return: La función `concur_idby_username` devuelve una lista de diccionarios.
    """
    list_params = [{
        "wstoken": api_key,
        "wsfunction": "core_user_get_users",
        "criteria[0][key]": "username",
        "criteria[0][value]": resultado
    } for resultado in resultados]

    return list_params


def concurr_matricular_usuario(resultados, roleid=5):
    """
    Esta función toma una lista de resultados e inscribe a los usuarios en un curso de Moodle.

    :param resultados: una lista de tuplas que contienen pares de ID de curso e ID de usuario para
    inscribir usuarios en Moodle

    :param roleid: El parámetro roleid es un parámetro opcional que especifica el rol del
    usuario que se inscribe en el curso. Toma un valor por defecto de 5, que corresponde
    al rol de "estudiante". Sin embargo, también se puede establecer en 3, que corresponde
    al "profesor con capacidad de edición".

    :return: una lista de diccionarios, donde cada diccionario contiene parámetros para inscribir
    a un usuario en un curso.
    """
    list_params = [{
        "wstoken": api_key,
        "moodlewsrestformat": "json",
        "wsfunction": "enrol_manual_enrol_users",
        "enrolments[0][roleid]": roleid,
        "enrolments[0][courseid]": resultado[0],
        "enrolments[0][userid]": resultado[1]
    } for resultado in resultados]

    return list_params


def concurr_desmatricular_usuario(resultados):
    """
    La función toma una lista de resultados y devuelve una lista de parámetros para dar de baja
    a los usuarios de un curso.

    :param resultados: Es una lista de tuplas que contienen la ID del curso y la ID de usuario
    de los usuarios que necesitan cancelar su inscripción en un curso.

    :return: una lista de diccionarios, donde cada diccionario contiene parámetros para dar de
    baja a los usuarios.
    """
    list_params = [{
        "wstoken": api_key,
        "moodlewsrestformat": "json",
        "wsfunction": "enrol_manual_unenrol_users",
        "enrolments[0][courseid]": resultado[0],
        "enrolments[0][userid]": resultado[1]
    } for resultado in resultados]

    return list_params


def ocultar_cursos(respuestas):
    """
    La función toma una lista de ID de cursos y devuelve una lista de parámetros para ocultar esos
    cursos.

    :param respuestas: Es una lista de ID de cursos que deben ocultarse.

    :return: una lista de diccionarios, donde cada diccionario contiene parámetros para una
    función de servicio web de Moodle "core_course_update_courses".
    """
    list_params = [{
        "wstoken": api_key,
        "moodlewsrestformat": "json",
        "wsfunction": "core_course_update_courses",
        "courses[0][id]": respuesta,
        "courses[0][visible]": 0
    } for respuesta in respuestas]

    return list_params


def listar_cursos_por_idcurso(respuestas):
    """
    La función toma una lista de ID de cursos y devuelve una lista de parámetros que se usarán
    para recuperar información sobre esos cursos.

    :param respuestas: Una lista de ID de cursos para recuperar información del curso.

    :return: una lista de diccionarios, donde cada diccionario contiene parámetros para recuperar
     cursos por su ID.
    """
    list_params = [{
        "wstoken": api_key,
        "moodlewsrestformat": "json",
        "wsfunction": "core_course_get_courses_by_field",
        "field": "id",
        "value": respuesta
    } for respuesta in respuestas]

    return list_params


def concurr_obtener_tareas(resultados): # pylint: disable=missing-docstring
    list_params = [{
        "wstoken": api_key,
        "moodlewsrestformat": "json",
        "wsfunction": "mod_assign_get_assignments",
        "courseids[0]": int(resultado),
        "includenotenrolledcourses": 1
    } for resultado in resultados]

    return list_params


def concurr_obtener_archivos(resultados): # pylint: disable=missing-docstring
    list_params = [{
        "wstoken": api_key,
        "moodlewsrestformat": "json",
        "wsfunction": "mod_resource_get_resources_by_courses",
        "courseids[0]": int(resultado)
    } for resultado in resultados]

    return list_params


def concurr_obtener_todos_recursos(resultados): # pylint: disable=missing-docstring
    list_params = [{
        "wstoken": api_key,
        "moodlewsrestformat": "json",
        "wsfunction": "core_course_get_contents",
        "courseid": int(resultado)
    } for resultado in resultados]

    return list_params


def obtener_todos_recursos_semana(curso_id): # pylint: disable=missing-docstring
    list_params = {
        "wstoken": api_key,
        "moodlewsrestformat": "json",
        "wsfunction": "core_course_get_contents",
        "courseid": int(curso_id)
    }

    response = session.post(f"{url}", params=list_params).json()
    resultado = defaultdict(lambda: defaultdict(int))

    for curso in response:
        for modulos in curso['modules']:
            resultado[curso['id'], curso['name']][modulos['modname']] += 1

    resultado = {f"{k[0]}, {k[1]}": dict(v) for k, v in resultado.items()}
    retorno = {curso_id: resultado}

    return retorno


def obtener_notas_curso(curso_id): # pylint: disable=missing-docstring
    list_params = {
        "wstoken": api_key,
        "moodlewsrestformat": "json",
        "wsfunction": "gradereport_user_get_grade_items",
        "courseid": int(curso_id)
    }

    response = session.post(f"{url}", params=list_params).json()
    return dict(response)
