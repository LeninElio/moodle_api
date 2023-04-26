# en este archivo estan algunas funciones pensadas inicialmente

# from funciones import moodle, sql
# import concurrent.futures
# import time
# import csv


# def lista_cursos_moodle():
#     query = f'''select parent from sva.le_ciclo'''

#     resultados = sql.lista_query(query)
#     lista_cursos = moodle.cursos_concurr_categoria(resultados)

#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         cursos = list(executor.map(moodle.creacion_concurrente, lista_cursos))

#     with open("./data/temp_data.csv", "a", newline='') as file:
#         writer = csv.writer(file)
#         for curso in cursos:
#             for shortname in curso['courses']:
#                 writer.writerow([shortname['shortname']])


# lista_cursos_moodle()


# obtener id de alumnos y cursos de moodle con username
# @principal.calcular_tiempo
# def obtener_alumnos_cursos():
#     query = f'''
#     SELECT
#         LOWER(r.Alumno) AS alumno,
#         concat ( c.Nombre, ', ', e.Abreviatura, ', ', cp.Semestre, ', ', cp.Seccion ) AS idcurso 
#     FROM
#         dbo.Rendimiento AS r
#         INNER JOIN dbo.Curso AS c ON r.Curricula = c.Curricula 
#         AND r.Curso = c.Curso 
#         AND r.Escuela = c.Escuela
#         INNER JOIN dbo.CursoProgramado AS cp ON c.Curricula = cp.Curricula 
#         AND c.Curso = cp.Curso 
#         AND c.Escuela = cp.Escuela 
#         AND r.Semestre = cp.Semestre 
#         AND r.Seccion = cp.Seccion
#         INNER JOIN dbo.Escuela AS e ON cp.Escuela = e.Escuela 
#     WHERE
#         r.Semestre = '2020-1';
#     '''

#     resultados = sql.lista_query(query)
#     lista_cursos = moodle.lista_concurr_byshortname(resultados)
#     lista_alumnos = moodle.lista_concurr_byusername(resultados)

#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         cursos = list(executor.map(moodle.creacion_concurrente, lista_cursos))
#         alumnos = list(executor.map(moodle.creacion_concurrente, lista_alumnos))

#     with open("./test_data/temp_data.txt", "a", encoding='utf-8') as file:
#         for matricula in zip(alumnos, cursos):
#             file.write(str(matricula) + "\n")


# obtener_alumnos_cursos()


# listar datos de txt con open
# @principal.calcular_tiempo
# def conwith():
#     with open('./test_data/temp_data.txt', 'r', encoding='utf-8') as file:
#         datos = file.readlines()
#         resultados = [[int(x) for x in dato.split(',')] for dato in datos]
    
#     return resultados

# # print(resultado)


# Listar datos de txt con pandas
# @principal.calcular_tiempo
# def pandita():
#     df = pd.read_csv('./test_data/temp_data.txt', header=None, names=['A', 'B'])
#     lista = df.values.tolist()
#     return lista


# conwith()
# pandita()


# def listar_datos_txt():
#     with open('./test_data/temp_data_copy.txt', 'r', encoding='utf-8') as archivo:
#         datos_objeto = [eval(linea) for linea in archivo]

#     for obj in datos_objeto:
#         print(obj)
#         # try:
#         #     id = obj[0]['users'][0]['id']
#         #     username = obj[0]['users'][0]['username']
#         #     email = obj[0]['users'][0]['email']
#         #     course_id = obj[1]['courses'][0]['id']
#         #     fullname = obj[1]['courses'][0]['fullname']
#         #     print(id, username, email, course_id, fullname)
#         # except (KeyError, IndexError):
#         #     print('Error: objeto no tiene la estructura esperada')
#         #     continue


# listar_datos_txt()

from funciones import moodle
from concurrent.futures import ThreadPoolExecutor
import asyncio


# Devuelve la lista de los usuario no creados en moodle usando asyncio
async def obtener_username(username):
    # Realizar llamada a la API de Moodle para obtener información del usuario
    existe = moodle.async_idby_username(username)
    if existe['users'] == []:
        return username
    else:
        return None


async def lista_alumnos():
    resultados = ['131.2502.153', '00.0018.n.ac', '00.0360.1.ad', '00.0496.5.ao', '00.0600.n.ad', '01.0147.6.dl', '01.0227.9.ah', '01.0234.8.an', '01.0284.1.eo', '02.0276.2.de', '02.0391.3.ar']

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
    resultados = ['131.2502.153', '00.0018.n.ac', '00.0360.1.ad', '00.0496.5.ao', '00.0600.n.ad', '01.0147.6.dl', '01.0227.9.ah', '01.0234.8.an', '01.0284.1.eo', '02.0276.2.de', '02.0391.3.ar']

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
    resultados = ['131.2502.153', '00.0018.n.ac', '00.0360.1.ad', '00.0496.5.ao', '00.0600.n.ad', '01.0147.6.dl', '01.0227.9.ah', '01.0234.8.an', '01.0284.1.eo', '02.0276.2.de', '02.0391.3.ar']
    
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
        # print(existe['users'][0]['id'])
        return (username, existe['users'][0]['id'])


def listar_matriculados():
    resultados = ['201.2904.009', '191.0105.034', '171.1006.002', '201.1006.004', '201.1205.035', '151.0505.470', '201.0906.045', '151.0403.050', '161.0904.259', '151.0802.223', '132.2901.457', '181.3602.049', '161.1203.664', '151.0103.187', '151.1905.348', '151.1604.461', '171.0306.027', '151.2502.055', '082.0904.344']
    
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(get_username_id, resultados))
    
    existe = [(username, exists) for username, exists in results if exists > 0]
    noexiste = [username for username, exists in results if not exists]
    
    # return (existe, noexiste)
    # print(f'{existe=}, {noexiste=}')
    print(existe)
    # print(noexiste)


listar_matriculados()