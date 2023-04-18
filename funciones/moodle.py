from dotenv import load_dotenv
import requests
import os

load_dotenv('private/.env')

api_key = os.getenv('API_KEY')
url = os.getenv('url')

global_params = {
    "wstoken": api_key,
    "moodlewsrestformat": "json"
}

session = requests.Session()

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


def cursos_por_id(id):
    list_params = {
        "wsfunction": "core_enrol_get_users_courses",
        "userid": id
    }

    params = {**global_params, **list_params, "moodlewsrestformat": "json"}
    response = session.get(f"{url}", params=params).json()
    retorno = [curso['shortname'] for curso in response]
    return retorno


def listar_categorias():
    list_params = {
        "wsfunction": "core_course_get_categories"
    }

    params = {**global_params, **list_params}
    response = session.get(f"{url}", params=params).json()
    retorno = [(cat['id'], cat['name']) for cat in response]
    return retorno


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


def cursos_por_username(username):
    return cursos_por_id(iduser_por_username(username))


def crear_categoria(cat_nombre, idnumber, cat_desc):
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
    list_params = {
        "wsfunction": "core_course_create_categories",
        "categories[0][name]": cat_nombre,
        "categories[0][idnumber]": idnumber,
        "categories[0][description]": cat_desc,
        "categories[0][parent]": parent_id
    }

    params = {**global_params, **list_params}
    response = session.post(f"{url}", params=params).json()
    # session.post(f"{url}", params=params).json()
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


# username, course_shortname, roleid = 5
def matricular_a_cursos(username, cursos, role_id):
    for curso in cursos:
        matricular_usuario(username, curso, role_id)


# username, course_shortname
def desmatricular_de_cursos(username, cursos):
    for curso in cursos:
        desmatricular_usuario(username, curso)


def crear_concurr_cursos(params):
    response = session.post(f"{url}", params=params).json()
    return response


def lista_concurr_cursos(resultados):
    list_params = [
        {
            "wstoken": api_key,
            "moodlewsrestformat": "json",
            "wsfunction": "core_course_create_courses",
            "courses[0][fullname]": resultado[0],
            "courses[0][shortname]": resultado[1],
            "courses[0][categoryid]": resultado[2],
            "courses[0][format]": 'weeks'
        } for resultado in resultados]

    return list_params