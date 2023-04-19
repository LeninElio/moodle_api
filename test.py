from funciones import moodle, sql
import concurrent.futures
import time

def matricular_alumnos():
    query = f'''
    SELECT
        lower(r.Alumno) as alumno,
        concat ( c.Nombre, ', ', e.Abreviatura, ', ', cp.Semestre, ', ', cp.Seccion ) AS idcurso 
    FROM
        dbo.Rendimiento AS r
        INNER JOIN dbo.Curso AS c ON r.Curricula = c.Curricula 
        AND r.Curso = c.Curso 
        AND r.Escuela = c.Escuela
        INNER JOIN dbo.CursoProgramado AS cp ON c.Curricula = cp.Curricula 
        AND c.Curso = cp.Curso 
        AND c.Escuela = cp.Escuela 
        AND r.Semestre = cp.Semestre 
        AND r.Seccion = cp.Seccion
        INNER JOIN dbo.Escuela AS e ON cp.Escuela = e.Escuela 
    WHERE
        r.Semestre = '2020-1' 
        AND r.Alumno IN ('00.0018.n.ac', '00.0360.1.ad', '00.0496.5.ao', '00.0600.n.ad')
    '''

    # try:

    resultados = sql.lista_query(query)
    # for resultado in resultados:
    #     print(resultado)
    lista_cursos = moodle.lista_concurr_byshortname(resultados)
    lista_alumnos = moodle.lista_concurr_byusername(resultados)

    # print(list_params)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        cursos = list(executor.map(moodle.creacion_concurrente, lista_cursos))
        alumnos = list(executor.map(moodle.creacion_concurrente, lista_alumnos))

    # # with open("./data/temp_data.txt", "a") as file:
    for matricula in zip(alumnos, cursos):
        matriculados = f"{matricula[0]['users'][0]['id']}, {matricula[1]['courses'][0]['id']}"
        print(matriculados)
    #         # file.write(str(matriculados) + "\n")
    
    # except Exception as e:
    #     return f'Fallaste {e}'


inicio = time.time()
matricular_alumnos()
fin = time.time()

print(f"Tiempo de ejecución: {fin - inicio} segundos")



