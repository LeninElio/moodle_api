from funciones import moodle, sql, funciones
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import json

# Semestre a crear
semestre = '2020-1'

# Creacion de la categoria principal
def crear_cat_semestre():

    try:
        name = f'Semestre {semestre}'  
        desc = f'Categoría para el semestre académico {semestre}'

        principal = moodle.crear_categoria(name, semestre, desc)
        data = {'nombre': semestre, 'nombre_completo': name, 'descripcion': desc, 'parent': principal[0]['id']}
        sql.insertar_datos('sva.le_semestre', data)
        print(data)

    except Exception as e:
        return f'Fallaste {e}'


# Creacion de la sub categoria facultades
def crear_cat_facultades():
    query = f'''
    SELECT
        CONCAT('{semestre}', '-', f.Facultad) cat_num, 
        CONCAT('FACULTAD DE ', f.Descripcion) as cat_name,
        CONCAT('CATEGORIA DE LA FACULTAD DE ', f.Descripcion) as cat_desc,
        f.Facultad
    FROM
        dbo.Facultad AS f
    WHERE f.Activo = '1' '''

    semestre_val = sql.informacion_semestre(semestre)

    try:
        resultados = sql.lista_query(query)

        for resultado in resultados:
            num = resultado[0]
            name = resultado[1]
            desc = resultado[2]
            idfac = resultado[3]
            
            facultades = moodle.crear_sub_categoria(name, num, desc, semestre_val[1])
            data = {'semestre': semestre_val[0], 'numeracion': num, 'parent': facultades[0]['id'], "idfac": idfac}
            sql.insertar_datos('sva.le_facultad', data)
            print(data)

    except Exception as e:
        return f'Fallaste {e}'


# Creacion de la sub categoria escuelas
def crear_cat_escuelas():
    semestre_val = sql.informacion_semestre(semestre)

    # Se le agrega algunas cosas al query para que la informacion sea mas legible
    query = f'''
    SELECT
        e.Descripcion as cat_name,
        CONCAT(f.numeracion, '-', e.Escuela) as num,
        CONCAT('ESCUELA PROFESIONAL DE ', e.Descripcion) as cat_desc,
        f.parent as parent,
        e.Escuela
    FROM
        dbo.Escuela AS e
        INNER JOIN sva.le_facultad AS f ON e.Facultad = f.idfac
    where e.Activo = '1' AND f.semestre = '{semestre_val[0]}' 
    '''

    try:
        resultados = sql.lista_query(query)
        for resultado in resultados:
            name = resultado[0]
            num = resultado[1]
            desc = resultado[2]
            parent = resultado[3]
            idesc = resultado[4]

            escuelas = moodle.crear_sub_categoria(name, num, desc, parent)
            data = {'semestre': semestre_val[0], 'numeracion': num, 'parent': escuelas[0]['id'], "idesc": idesc}
            sql.insertar_datos('sva.le_escuela', data)
            print(data)

    except Exception as e:
        return f'Fallaste {e}'


# Creacion de la sub categoria ciclos
def crear_cat_ciclos():
    query = f'''
    SELECT
        cp.Escuela,
        c.Ciclo,
        le.parent,
        concat ( le.numeracion, '-', c.Ciclo ) AS numeracion 
    FROM
        dbo.CursoProgramado AS cp
        INNER JOIN dbo.Curso AS c ON c.Curso = cp.Curso 
        AND cp.Escuela = c.Escuela 
        AND cp.Curricula = c.Curricula
        INNER JOIN sva.le_escuela le ON le.idesc = cp.Escuela 
    WHERE
        cp.Semestre = '{semestre}' 
    GROUP BY
        cp.Escuela,
        c.Ciclo,
        le.parent,
        le.numeracion 
    '''

    try:
        resultados = sql.lista_query(query)
        for resultado in resultados:
            # print(resultado)
            ciclos = moodle.crear_sub_categoria(resultado[1], resultado[3], resultado[1], resultado[2])
            data = {'numeracion': resultado[3], 'parent': ciclos[0]['id'], "idescparent": resultado[2], "idciclo": resultado[1]}
            sql.insertar_datos('sva.le_ciclo', data)
            print(data)

    except Exception as e:
        return f'Fallaste {e}'


# Creacion de la sub categoria ciclos
def crear_cursos():
    query = f'''
    SELECT
        concat ( cp.Semestre, ', ', c.Nombre, ', ', e.Abreviatura, ', ', cp.Seccion ) AS nombrecompleto,
        concat ( c.Nombre, ', ', e.Abreviatura, ', ', cp.Semestre, ', ', cp.Seccion ) AS idcurso,
        lc.parent 
    FROM
        dbo.CursoProgramado AS cp
        INNER JOIN dbo.Curso AS c ON cp.Curricula = c.Curricula 
        AND cp.Curso = c.Curso 
        AND cp.Escuela = c.Escuela
        INNER JOIN sva.le_escuela AS le ON c.Escuela = le.idesc
        INNER JOIN sva.le_ciclo AS lc ON le.parent = lc.idescparent 
        AND c.Ciclo = lc.idciclo
        INNER JOIN dbo.Escuela AS e ON c.Escuela = e.Escuela 
    WHERE
        cp.Semestre = '{semestre}'
    '''

    try:
        resultados = sql.lista_query(query)
        list_params = moodle.lista_concurr_cursos(resultados)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            responses = list(executor.map(moodle.creacion_concurrente, list_params))

        return responses
    
    except Exception as e:
        return f'Fallaste {e}'
    

def crear_usuarios():
    query = f'''
    SELECT DISTINCT
        a.alumno,
        a.password,
        a.nombre,
        a.apellido,
        a.email
    FROM
        le_correolimpio AS a
    WHERE
        (a.email <> '' or a.email IS NULL)
        AND CHARINDEX('@', a.email) > 0
        AND CHARINDEX('.', a.email, CHARINDEX('@', a.email)) > 0
        AND CHARINDEX(' ', a.email) = 0
        AND PATINDEX('%[,"()<>;[]]%', a.email) = 0
    GROUP BY
        a.email,
    a.alumno,
        a.password,
        a.nombre,
        a.apellido
    '''

    try:
        resultados = sql.lista_query(query)
        list_params = moodle.lista_concurr_usuarios(resultados)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            responses = list(executor.map(moodle.creacion_concurrente, list_params))

        return responses
    
    except Exception as e:
        return f'Fallaste {e}'


def matricular_alumnos(func):
    def ejecutor():
        try:
            matriculados = func()
            lista_matriculados = moodle.lista_concurr_matriculas(matriculados)
            with concurrent.futures.ThreadPoolExecutor() as executor:
                responses = list(executor.map(moodle.creacion_concurrente, lista_matriculados))

            return responses
        
        except Exception as e:
            return f'Fallaste en matricular_alumnos {e}'
    return ejecutor
    

def get_username_id(username):
    existe = moodle.async_idby_username(username)
    
    if existe['users'] == []:
        return (username, False)
    else:
        return (username, existe['users'][0]['id'])


def get_idcourseby_shortname(shortname):
    existe = moodle.async_idby_shortname(shortname)
    
    if existe['courses'] == []:
        return (shortname, False)
    else:
        return (shortname, existe['courses'][0]['id'])


def actualizar_iduserpor_lotes(alumnos):
    sql.ejecutar("CREATE TABLE sva.le_alumnos (nombreusuario VARCHAR(20), moodle_id INT)")

    for alumno in alumnos:
        data = {'nombreusuario': alumno[0], 'moodle_id': alumno[1]}
        sql.insertar_datos('sva.le_alumnos', data)
    
    sql.ejecutar("""
        UPDATE a
        SET a.moodle_id = la.moodle_id
        FROM dbo.Alumno as a
        INNER JOIN sva.le_alumnos as la
        ON a.Alumno = la.nombreusuario
    """)
    
    sql.ejecutar("DROP TABLE IF EXISTS sva.le_alumnos")


def crear_usuario_restante(lista):
    usuarios = "', '".join(lista)

    query = f'''
    SELECT
        Alumno AS username,
        TRIM ( Password ) AS password,
        Nombre AS nombre,
        CONCAT ( ApellidoPaterno, ' ', ApellidoMaterno ) AS apellido,
        LOWER (
            CONCAT (
                dbo.eliminar_acentos ( SUBSTRING ( ApellidoPaterno, 1, 2 ) ),
                dbo.eliminar_acentos ( ApellidoMaterno ),
                dbo.eliminar_acentos ( SUBSTRING ( Nombre, 1, 2 ) ),
                '@unasam.edu.pe' 
            ) 
        ) AS correo 
    FROM
        dbo.Alumno AS a 
    WHERE
        Alumno IN ('{usuarios}')
    '''

    resultados = sql.lista_query(query)
    
    try:
        list_params = moodle.lista_concurr_usuarios(resultados)

        with ThreadPoolExecutor() as executor:
            responses = list(executor.map(moodle.creacion_concurrente, list_params))

        return responses
    
    except Exception as e:
        return e


# @funciones.calcular_tiempo
def insertar_id_alumno():
    query = f'''
    SELECT DISTINCT
        LOWER(r.Alumno) AS alumno 
    FROM
        dbo.Rendimiento AS r
        INNER JOIN dbo.Alumno AS a ON r.Alumno = a.Alumno 
    WHERE
        a.moodle_id IS NULL 
        AND r.Semestre = '{semestre}'
    '''
    
    resultados = sql.lista_query_especifico(query)

    try:
        if resultados != []:
            with ThreadPoolExecutor() as executor:
                results = list(executor.map(get_username_id, resultados))
        
            existe = [(username, exists) for username, exists in results if exists > 0]
            noexiste = [username for username, exists in results if not exists]

            actualizar_iduserpor_lotes(existe)
            crear_usuario_restante(noexiste)
            print(noexiste)

        else:
            print('No hay mas datos')

    except Exception as e:
            return e


def actualizar_idcoursepor_lotes(alumnos):
    sql.ejecutar("CREATE TABLE sva.le_courses_temp (nombrecorto VARCHAR(255), id_moodle INT)")

    for alumno in alumnos:
        data = {'nombrecorto': alumno[0], 'id_moodle': alumno[1]}
        sql.insertar_datos('sva.le_courses_temp', data)
    
    sql.ejecutar("""
        UPDATE lc 
        SET lc.id_moodle = lct.id_moodle 
        FROM
            sva.le_cursos AS lc
            INNER JOIN sva.le_courses_temp AS lct 
            ON lc.nombrecorto = lct.nombrecorto
    """)
    
    sql.ejecutar("DROP TABLE IF EXISTS sva.le_courses_temp")


def crear_curso_restante(lista):
    cursos = "', '".join(lista)

    query = f'''
    SELECT
        nombrecompleto, 
        nombrecorto, 
        categoriaid, 
        fechainicio, 
        idcurso
    FROM
        sva.le_cursos AS lc
    WHERE
        lc.nombrecorto IN ('{cursos}')
    '''

    resultados = sql.lista_query(query)

    try:
        list_params = moodle.lista_concurr_cursos(resultados)
        with ThreadPoolExecutor() as executor:
            responses = list(executor.map(moodle.creacion_concurrente, list_params))

        print(list_params)
        return responses
    
    except Exception as e:
        return e


@funciones.calcular_tiempo
def insertar_id_curso():
    query = f'''
    SELECT 
        lc.nombrecorto
    FROM
        sva.le_cursos AS lc
    WHERE
        lc.semestre = '{semestre}' and 
        lc.id_moodle is null  
    '''
    
    resultados = sql.lista_query_especifico(query)

    try:
        if resultados != []:
            with ThreadPoolExecutor() as executor:
                results = list(executor.map(get_idcourseby_shortname, resultados))

            existe = [(username, exists) for username, exists in results if exists > 0]
            noexiste = [username for username, exists in results if not exists]

            actualizar_idcoursepor_lotes(existe)
            crear_curso_restante(noexiste)

        else:
            print('No hay mas datos')

    except Exception as e:
            return e


def insertar_matriculas_bd(matriculas):
    with sql.obtener_cursor() as cursor:
        for matricula in matriculas:
            data = {'curso_id': matricula[0], 'alumno_id': matricula[1]}
            
            cursor.execute('INSERT INTO sva.le_maticulas_moodle (curso_id, alumno_id) VALUES (%s, %s)', (data['curso_id'], data['alumno_id']))
            
    return 'Completo'

    
# funcion que permite obtener a los alumnos y sus cursos matriculados a partir de un id curso mas rapido
@funciones.calcular_tiempo_arg
def obtener_matriculas_moodle():
    query = "SELECT top 3 lc.id_moodle from sva.le_cursos lc"
    
    cursos = sql.lista_query_especifico(query)

    try:
        if cursos != []:

            list_params = moodle.async_peticion_por_idcurso(cursos)
            
            with ThreadPoolExecutor() as executor:
                responses = list(executor.map(moodle.creacion_concurrente, list_params))

            matriculas = [(cursos['id'], matriculados['id']) for resultado in responses for matriculados in resultado for cursos in matriculados['enrolledcourses']]

            # print(matriculas)

            insertar_matriculas_bd(matriculas)

        else:
            print('No hay cursos')

    except Exception as e:
            return e


def transformar_dataframe(dataframe):
    obtenidos = []
    for col in dataframe.columns:
        for row in dataframe[col]:
            if row is not None and 'id' in row:
                cursos = [curso['id'] for curso in row['enrolledcourses'] if 'id' in curso] if row['enrolledcourses'] is not None else []
                obtenidos.append([(curso, row['id']) for curso in cursos])

    obtenido = [ids for lista in obtenidos for ids in lista]
    # daf = pd.DataFrame(obtenido, columns=['curso', 'id'])
    return obtenido


@funciones.calcular_tiempo_arg
def obtener_matriculas_moodle_pandas():
    query = "SELECT lc.id_moodle from sva.le_cursos lc"
    
    cursos = sql.lista_query_especifico(query)

    try:
        if cursos != []:

            list_params = moodle.async_peticion_por_idcurso(cursos)
            
            with ThreadPoolExecutor() as executor:
                responses = list(executor.map(moodle.creacion_concurrente, list_params))

            json_data = json.dumps(responses)
            df = pd.read_json(json_data)

            matriculas = transformar_dataframe(df)

            print(len(matriculas))

            insertar_matriculas_bd(matriculas)

        else:
            print('No hay cursos')

    except Exception as e:
            return e


obtener_matriculas_moodle_pandas()