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
