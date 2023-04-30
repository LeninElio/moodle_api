from funciones import moodle, sql, funciones, migracion
from concurrent.futures import ThreadPoolExecutor
import datetime
import concurrent.futures
import pandas as pd
import json

# Semestre a crear
# semestre = '2020-1'

# Creacion de la categoria principal (semestre)
@funciones.calcular_tiempo_arg
def crear_semestre(semestre):
    try:
        name = f'Semestre {semestre}'  
        desc = f'Categoría para el semestre académico {semestre}'

        nuevo_semestre = moodle.crear_categoria(name, semestre, desc)

        if 'exception' in nuevo_semestre:
            return f"Error en la creacion del semestre, {nuevo_semestre['message']}"
        
        else:
            data = {'nombre': semestre, 'nombre_completo': name, 'descripcion': desc, 'parent': nuevo_semestre[0]['id']}
            sql.insertar_datos('sva.le_semestre', data)
            
            return 'Semestre creado exitosamente'

    except Exception as e:
        return f'Fallo en la creacion del semestre, Error: {e}'


# Creacion de la sub categoria facultades
@funciones.calcular_tiempo_arg
def crear_facultades(semestre):
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
            
            if 'exception' in facultades:
                return f"Error en la creacion de facultades, {facultades['message']}"
            
            else:
                data = {'semestre': semestre_val[0], 'numeracion': num, 'parent': facultades[0]['id'], "idfac": idfac}
                
                sql.insertar_datos('sva.le_facultad', data)

        return 'Facultades creados satisfactoriamente'

    except Exception as e:
        return f'Error en la creacion de facultades, Error: {e}'


# Creacion de la sub categoria escuelas
@funciones.calcular_tiempo_arg
def crear_escuelas(semestre):
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

            if 'exception' in escuelas:
                return f"Error en la creacion de escuelas, {escuelas['message']}"
                
            else:
                data = {'semestre': semestre_val[0], 'numeracion': num, 'parent': escuelas[0]['id'], "idesc": idesc}

                sql.insertar_datos('sva.le_escuela', data)

        return 'Escuelas creadas satisfactoriamente.'

    except Exception as e:
        return f'Error en la creacion de escuelas, Error: {e}'


# Creacion de la sub categoria ciclos
def crear_ciclos(semestre):
    semestre_val = sql.informacion_semestre(semestre)

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
        AND le.semestre = '{semestre_val[0]}' 
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
            ciclos = moodle.crear_sub_categoria(resultado[1], resultado[3], resultado[1], resultado[2])

            if 'exception' in ciclos:
                return f"Error en la creacion de ciclos, {ciclos['message']}"
            
            else:
                data = {'numeracion': resultado[3], 'parent': ciclos[0]['id'], "idescparent": resultado[2], "idciclo": resultado[1]}
                sql.insertar_datos('sva.le_ciclo', data)

        return 'Ciclos creados satisfactoriamente.'

    except Exception as e:
        return f'Error en la creacion de ciclos, Error: {e}'


# Inicio de clases debe ser en formato AÑO-MES-DIA (2023-04-29)
@funciones.calcular_tiempo_arg
def migracion_cursos_bd(semestre = None, inicioclases = None):
    if semestre is None or inicioclases is None:
        return 'Ingrese los valores del Semestre y la fecha de inicio de clases'

    semestre_val = sql.informacion_semestre(semestre)

    if semestre_val is None:
        return 'El semestre mencionado no existe.'
    
    try:
        fecha_verificada = datetime.datetime.strptime(inicioclases, '%Y-%m-%d')

        sql.ejecutar(f"""
            INSERT INTO sva.le_cursos (nombrecompleto, nombrecorto, categoriaid, fechainicio, semestre, idcurso)
            SELECT
                concat ( cp.Semestre, ', ', c.Nombre, ', ', e.Abreviatura, ', ', cp.Seccion ) AS nombrecompleto,
                concat ( c.Nombre, ', ', e.Abreviatura, ', ', cp.Semestre, ', ', cp.Seccion ) AS nombrecorto,
                lc.parent as categoriaid,
                DATEDIFF(SECOND, '1970-01-01 00:00:00.0', '{fecha_verificada}') as fechainicio,
                cp.Semestre,
                concat (cp.Semestre, '-', le.idesc, c.Curricula, cp.Seccion, '-', c.Curso) as idcurso
            FROM
                dbo.CursoProgramado AS cp
                INNER JOIN dbo.Curso AS c ON cp.Curricula = c.Curricula 
                AND cp.Curso = c.Curso 
                AND cp.Escuela = c.Escuela
                INNER JOIN sva.le_escuela AS le ON c.Escuela = le.idesc
                AND le.semestre = {semestre_val[0]} 
                INNER JOIN sva.le_ciclo AS lc ON le.parent = lc.idescparent 
                AND c.Ciclo = lc.idciclo
                INNER JOIN dbo.Escuela AS e ON c.Escuela = e.Escuela 
            WHERE
                cp.Semestre = '{semestre}'
        """)
        
        return 'Migracion de cursos completo.'
    
    except ValueError:
        return 'Error: La fecha debe tener el formato "año-mes-día"'
    


# Creacion de cursos
def crear_cursos(semestre):
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
        lc.Semestre = '{semestre}'
    '''

    try:
        resultados = sql.lista_query(query)
        list_params = moodle.lista_concurr_cursos(resultados)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(moodle.creacion_concurrente, list_params)
            # responses = list(executor.map(moodle.creacion_concurrente, list_params))

        # return responses
        return 'Cursos creados satisfactoriamente.'
    
    except Exception as e:
        return f'Error en la creacion de cursos, Error: {e}'
    

"""
# Nota (Lenin Elio - 29/04/2023 16:00)
# Busqueda e insersion de cursos restantes
# Las funciones a continuacion estan creadas para la busqueda e insersion de cursos
# que no llegaron a insertarse por el uso de funciones asincronas
"""


# Subproceso: crear cursos restantes en moodle
def crear_curso_restante_moodle(lista):
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
            executor.map(moodle.creacion_concurrente, list_params)
            # responses = list(executor.map(moodle.creacion_concurrente, list_params))

        return 'Subproceso: Cursos restantes creados en moodle.'
    
    except Exception as e:
        return f'Subproceso: Error en la creacion de cursos restantes, Error: {e}'


# Insertar el id del curso de moodle en la base de datos para el manejo de matriculas
def insertar_idcurso_moodle_bd(alumnos):
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

    return 'Subproceso: Ids cursos insertados de moodle a bd.'


# Obtener el id del curso por el nombre corto del curso
def obtener_idcurso_pornombre(shortname):
    existe = moodle.async_idby_shortname(shortname)
    
    if existe['courses'] == []:
        return (shortname, False)
    else:
        return (shortname, existe['courses'][0]['id'])
    

# Funcion principal para la correccion de cursos restantes 
@funciones.calcular_tiempo_arg
def corregir_cursos_noinsertados(semestre):
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
                results = list(executor.map(obtener_idcurso_pornombre, resultados))

            existe = [(username, exists) for username, exists in results if exists > 0]
            noexiste = [username for username, exists in results if not exists]

            insertar_idcurso_moodle_bd(existe)
            crear_curso_restante_moodle(noexiste)

            return f'Cursos pendientes por insertar: {len(noexiste)}'

        else:
            return 'No hay mas cursos por corregir.'

    except Exception as e:
            return f'Error en la correccion de cursos, Error: {e}'


"""
# Nota (Lenin Elio - 29/04/2023 16:05)
# Fin de busqueda e insersion de cursos restantes
"""


# Ejecutar solo si no tiene ningun usuario creado en moodle, si ya hay de un semestre acterior
# usar la funcion de actualizacion 
def crear_usuarios(semestre):
    query = f'''
    EXEC le_datos_matriculados '{semestre}'
    '''

    try:
        resultados = sql.lista_query(query)
        list_params = moodle.lista_concurr_usuarios(resultados)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            responses = list(executor.map(moodle.creacion_concurrente, list_params))

        return responses
    
    except Exception as e:
        return f'Fallaste {e}'


"""
# Nota (Lenin Elio - 29/04/2023 17:30)
# Busqueda e insersion de alumnos restantes
# Las funciones a continuacion estan creadas para la busqueda e insersion de alumnos
# que no llegaron a insertarse por el uso de funciones asincronas
"""


def obtener_idusuario_username(username):
    existe = moodle.async_idby_username(username)
    
    if existe['users'] == []:
        return (username, False)
    else:
        return (username, existe['users'][0]['id'])


def insertar_iduser_moodle_bd(alumnos):
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

    return 'Subproceso: IDs de alumnos insertados.'


def crear_usuario_restante(lista):
    usuarios = "', '".join(lista)

    query = f'''
    SELECT LOWER
        ( Alumno ) AS username,
        TRIM ( Password ) AS password,
        Nombre AS nombre,
        CONCAT ( ApellidoPaterno, ' ', ApellidoMaterno ) AS apellido,
        LOWER (
            REPLACE(
                CONCAT (
                    dbo.eliminar_acentos ( SUBSTRING ( ApellidoPaterno, 1, 2 ) ),
                    -- '_',
                    dbo.eliminar_acentos ( ApellidoMaterno ),
                    dbo.eliminar_acentos ( SUBSTRING ( Nombre, 1, 2 ) ),
                    '@unasam.edu.pe' 
                ),
                ' ', ''	
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
            problemas = list(executor.map(moodle.creacion_concurrente, list_params))
        
        if 'exception' in problemas:
            print(problemas)

        return 'Subproceso: Usuarios restantes creados.'
    
    except Exception as e:
        return f'Subproceso: Error en la creacion de usuarios restantes, {e}'


# Esta funcion en conjunto con sus subprocesos corrige a los alumnos no insertados por algun motivo
@funciones.calcular_tiempo_arg
def corregir_alumno_noinsertado(semestre):
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
                results = list(executor.map(obtener_idusuario_username, resultados))
        
            existe = [(username, exists) for username, exists in results if exists > 0]
            noexiste = [username for username, exists in results if not exists]

            insertar_iduser_moodle_bd(existe)
            crear_usuario_restante(noexiste)
            
            return f'Alumnos pendientes por insertar: {len(noexiste)}'

        else:
            return 'No hay mas datos a corregir.'

    except Exception as e:
            return f'Error en la correccion de alumnos, error: {e}'


"""
# Nota (Lenin Elio - 29/04/2023 17:39)
# Fin de busqueda e insersion de alumnos
"""


# matricular estudiantes
@funciones.calcular_tiempo_arg
def matricular_usuarios(semestre, alumno = None):
    if alumno is None:
        query = f''' EXEC le_matriculados '{semestre}' '''

    else:
        query = f''' EXEC le_matriculados '{semestre}', '{alumno}' '''
    
    resultados = sql.lista_query(query)

    try:
        if resultados != []:

            list_params = moodle.concurr_matricular_usuario(resultados)

            with ThreadPoolExecutor() as executor:
                executor.map(moodle.creacion_concurrente, list_params)
                # responses = list(executor.map(moodle.creacion_concurrente, list_params))

            return 'Matriculas realizadas con exito.'
        
        else:
            return 'No hay matriculas a realizar.'

    except Exception as e:
            return f'Error en las matriculas, error: {e}'


"""
# Nota (Lenin Elio - 29/04/2023 21:50)
# Busqueda e insersion de matriculas
# Las funciones a continuacion estan creadas para obtener las matriculas
# desde moodle y luego hacer la insercion en la base de datos
# esto con el fin de conocer que matriculas no se ejecutaron
"""


def insertar_matriculas_bd(matriculas, semestre):
    
    with sql.obtener_cursor() as cursor:
        for matricula in matriculas:
            data = {'curso_id': matricula[0], 'alumno_id': matricula[1], 'semestre_id': semestre}
            
            cursor.execute('INSERT INTO sva.le_maticulas_moodle (curso_id, alumno_id, semestre_id) VALUES (%s, %s, %s)', (data['curso_id'], data['alumno_id'], data['semestre_id']))
            
    return 'Se completo la insersion de datos obtenidos.'


def transformar_dataframe(dataframe):
    obtenidos = []
    for col in dataframe.columns:
        for row in dataframe[col]:
            if row is not None and 'id' in row:
                cursos = [curso['id'] for curso in row['enrolledcourses'] if 'id' in curso] if row['enrolledcourses'] is not None else []
                obtenidos.append([(curso, row['id']) for curso in cursos])

    obtenido = [ids for lista in obtenidos for ids in lista]
    return obtenido


@funciones.calcular_tiempo_arg
def obtener_matriculas_moodle_pandas(semestre):
    semestre_val = sql.informacion_semestre(semestre)
    query = f"SELECT lc.id_moodle from sva.le_cursos lc where lc.semestre = '{semestre}'"
    
    cursos = sql.lista_query_especifico(query)

    try:
        if cursos != []:
            list_params = moodle.async_peticion_por_idcurso(cursos)
            
            with ThreadPoolExecutor() as executor:
                responses = list(executor.map(moodle.creacion_concurrente, list_params))

            json_data = json.dumps(responses)
            df = pd.read_json(json_data)

            matriculas = transformar_dataframe(df)
            insertar_matriculas_bd(matriculas, semestre_val[0])

            return f'Se ha procesado {len(matriculas)} matriculas'

        else:
            return 'Parece que hay un error en el semestre.'

    except Exception as e:
            return e


"""
# Nota (Lenin Elio - 29/04/2023 21:55)
# Fin de busqueda e insersion de matriculas
"""
