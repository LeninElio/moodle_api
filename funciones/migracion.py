"""
Este módulo contiene funciones que interactuan con la API de moodle y la base de datos
"""

from concurrent.futures import ThreadPoolExecutor, wait
import datetime
import concurrent.futures
import json
import os
import requests
import pandas as pd
from funciones import decorador, moodle, sql


@decorador.calcular_tiempo_arg
def crear_semestre(semestre):
    """
    Esta función crea una nueva categoría de semestre en Moodle e inserta sus datos en una tabla
    de base de datos SQL.

    :param semestre: El parámetro "semestre" es una variable que representa el semestre académico
    para el cual se está creando una categoría. Se utiliza para generar el nombre y la
    descripción de la categoría.

    :return: un mensaje que indica si el semestre se creó con éxito o no.
    """
    try:
        name = f'Semestre {semestre}'
        desc = f'Categoría para el semestre académico {semestre}'

        nuevo_semestre = moodle.crear_categoria(name, semestre, desc)

        if 'exception' in nuevo_semestre:
            return f"Error en la creacion del semestre, {nuevo_semestre['message']}"

        # else:
        data = {
            'nombre': semestre,
            'nombre_completo': name,
            'descripcion': desc,
            'parent': nuevo_semestre[0]['id']
        }

        sql.insertar_datos('sva.le_semestre', data)
        return 'Semestre creado exitosamente'

    except requests.exceptions.RequestException as error:
        return f'Fallo en la creacion del semestre, Error: {error}'


@decorador.calcular_tiempo_arg
def crear_facultades(semestre):
    """
    Esta función crea subcategorías en Moodle para cada facultad activa en un semestre determinado e
    inserta datos en una tabla de base de datos.

    :param semestre: El parámetro "semestre" es una cadena que representa un semestre académico
    específico.

    :return: un mensaje que indica si la creación de facultades fue exitosa o no. Si hubo un error,
    el mensaje incluirá detalles sobre el error.
    """
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

            data = {
                'semestre': semestre_val[0],
                'numeracion': num,
                'parent': facultades[0]['id'],
                "idfac": idfac
            }

            sql.insertar_datos('sva.le_facultad', data)

        return 'Facultades creados satisfactoriamente'

    except requests.exceptions.RequestException as error:
        return f'Error en la creacion de facultades, error: {error}'


@decorador.calcular_tiempo_arg
def crear_escuelas(semestre):
    """
    Esta función crea categorías en Moodle basadas en información de la base de datos.

    :param semestre: El parámetro "semestre" es una cadena que representa el semestre académico
    para el cual se deben crear las escuelas.

    :return: un mensaje que indica si la creación de escuelas fue exitosa o no. Si hubo un error, el
    mensaje incluirá detalles sobre el error.
    """
    semestre_val = sql.informacion_semestre(semestre)
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

            data = {
                'semestre': semestre_val[0],
                'numeracion': num,
                'parent': escuelas[0]['id'],
                "idesc": idesc
            }

            sql.insertar_datos('sva.le_escuela', data)

        return 'Escuelas creadas satisfactoriamente.'

    except requests.exceptions.RequestException as error:
        return f'Error en la creacion de escuelas, error: {error}'


@decorador.calcular_tiempo_arg
def crear_ciclos(semestre):
    """
    Esta función crea ciclos en Moodle basados en información de una base de datos SQL.

    :param semestre: El parámetro "semestre" es una cadena que representa un semestre específico.
    Se utiliza para recuperar información sobre los cursos ofrecidos en ese semestre y
    crear categorías correspondientes para esos cursos en un sistema de gestión de aprendizaje

    :return: ya sea una cadena que indica que los ciclos se crearon con éxito o un mensaje de
    error si hubo un error en el proceso.
    """
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
        AND cp.tipo != 'H'
    GROUP BY
        cp.Escuela,
        c.Ciclo,
        le.parent,
        le.numeracion
    '''

    try:
        resultados = sql.lista_query(query)
        for resul in resultados:
            ciclos = moodle.crear_sub_categoria(resul[1], resul[3], resul[1], resul[2])

            if 'exception' in ciclos:
                return f"Error en la creacion de ciclos, {ciclos['message']}"

            data = {
                'numeracion': resul[3],
                'parent': ciclos[0]['id'],
                "idescparent": resul[2],
                "idciclo": resul[1]
            }
            sql.insertar_datos('sva.le_ciclo', data)

        return 'Ciclos creados satisfactoriamente.'

    except requests.exceptions.RequestException as error:
        return f'Error en la creacion de ciclos, error: {error}'


@decorador.calcular_tiempo_arg
def migracion_cursos_bd(semestre=None, inicioclases=None):
    """
    Esta función migra cursos de una base de datos a otra, dado un semestre y una fecha de inicio.

    :param semestre: El semestre para el cual se están migrando los cursos. Es un parámetro
    obligatorio.

    :param inicioclases: La fecha de inicio de clases del semestre en el formato "AAAA-MM-DD"

    :return: un mensaje de cadena que indica el éxito o el fracaso del proceso de migración.
    """
    if semestre is None or inicioclases is None:
        return 'Ingrese los valores del Semestre y la fecha de inicio de clases'

    semestre_val = sql.informacion_semestre(semestre)

    if semestre_val is None:
        return 'El semestre mencionado no existe.'

    try:
        fecha_verificada = datetime.datetime.strptime(inicioclases, '%Y-%m-%d')

        sql.ejecutar(f"""
            INSERT INTO sva.le_cursos
            (nombrecompleto, nombrecorto, categoriaid, fechainicio, semestre, idcurso, docente_id)
            SELECT
                concat ( cp.Semestre, ', ', c.Nombre, ', ', c.Curricula, ', ',
                     e.Abreviatura, ', ', cp.Seccion ) AS nombrecompleto,
                concat ( c.Nombre, ', ', e.Abreviatura, ', ', c.Curricula, ', ',
                     cp.Semestre, ', ', cp.Seccion ) AS nombrecorto,
                lc.parent AS categoriaid,
                DATEDIFF( SECOND, '1970-01-01 00:00:00.0', '{fecha_verificada}' ) AS fechainicio,
                cp.Semestre,
                concat ( cp.Semestre, '-', CAST ( c.id AS VARCHAR ), '-',
                CAST ( cp.CursoProgramado AS VARCHAR ) ) AS idcurso,
                t.moodle_id as docente_id
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
                INNER JOIN sva.le_semestre AS ls ON le.semestre = ls.id 
                AND cp.Semestre = ls.nombre
                INNER JOIN dbo.Trabajador AS t ON cp.Trabajador = t.Trabajador 
            WHERE
                cp.Semestre = '{semestre}' AND cp.tipo != 'H' 
        """)

        return 'Migracion de cursos completo.'

    except ValueError:
        return 'Error: La fecha debe tener el formato "año-mes-día"'


@decorador.calcular_tiempo_arg
def crear_cursos(semestre):
    """
    Esta función crea cursos en Moodle para un semestre dado usando programación concurrente.

    :param semestre: El parámetro "semestre" es una cadena que representa el semestre para
    el cual se están creando los cursos.

    :return: un mensaje de cadena que dice "Cursos creados satisfactoriamente".
    """
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

        return 'Cursos creados satisfactoriamente.'

    except requests.exceptions.RequestException as error:
        return f'Error en la creacion de cursos, error: {error}'


# Nota (Lenin Elio - 29/04/2023 16:00)
# Busqueda e insersion de cursos restantes
# Las funciones a continuacion estan creadas para la busqueda e insersion de cursos
# que no llegaron a insertarse por el uso de funciones asincronas


def crear_curso_restante_moodle(lista):
    """
    Esta función crea cursos de Moodle para una lista de cursos que aún no se han creado en Moodle.

    :param lista: El parámetro "lista" es una lista de cadenas que contienen los nombres de
    los cursos que se crearán en Moodle

    :return: un mensaje de cadena que indica si la creación de los cursos restantes en Moodle fue
    exitosa o si hubo un error.
    """
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

        return 'Subproceso: Cursos restantes creados en moodle.'

    except requests.exceptions.RequestException as error:
        return f'Subproceso: Error en la creacion de cursos restantes, error: {error}'


def insertar_idcurso_moodle_bd(cursos):
    """
    Esta función inserta los ID de los cursos de Moodle en una tabla de la base de datos y
    actualiza los registros correspondientes en otra tabla.

    :param cursos: Es una lista de tuplas que contiene el nombre de un curso y su ID de Moodle
    correspondiente

    :return: a string message: 'Subproceso: Ids cursos insertados de moodle a bd.'
    """
    sql.ejecutar("CREATE TABLE sva.le_courses_temp (nombrecorto VARCHAR(255), id_moodle INT)")

    query = 'INSERT INTO sva.le_courses_temp (nombrecorto, id_moodle) VALUES (%d, %d)'
    sql.insertar_muchos(query, cursos)

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


def obtener_idcurso_pornombre(shortname):
    """
    Esta función de Python obtiene el ID de un curso por su nombre corto en Moodle.

    :param shortname: El nombre abreviado de un curso de Moodle, que es un identificador
    único para el curso

    :return: una tupla con dos valores: el parámetro de entrada `shortname` y `False`
    si no hay cursos con ese shortname, o el `id` del primer curso que coincide con el
    shortname.
    """
    existe = moodle.async_idby_shortname(shortname)

    if existe['courses'] == []:
        return (shortname, False)
    else:
        return (shortname, existe['courses'][0]['id'])


@decorador.calcular_tiempo_arg
def corregir_cursos_noinsertados(semestre):
    """
    Esta función corrige los cursos que no se insertaron en Moodle consultando la base
    de datos de cursos con un semestre específico y sin ID de Moodle, luego usa
    subprocesos múltiples para obtener la ID de Moodle para los cursos existentes
    y crea los cursos restantes en Moodle.

    :param semestre: El semestre para el cual los cursos necesitan ser corregidos.

    :return: una cadena que indica la cantidad de cursos pendientes de insertar en Moodle.
    """
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

        return 'No hay mas cursos por corregir.'

    except requests.exceptions.RequestException as error:
        return f'Error en la correccion de cursos, Error: {error}'


# Nota (Lenin Elio - 29/04/2023 16:05)
# Fin de busqueda e insersion de cursos restantes


# Ejecutar solo si no tiene ningun usuario creado en moodle, si ya hay de un semestre acterior
# usar la funcion de actualizacion
def crear_usuarios(semestre):
    """
    Esta función crea usuarios al mismo tiempo utilizando datos de una consulta SQL
    y una API de Moodle.

    :param semestre: El parámetro "semestre" es una cadena que representa el semestre
    académico para el
    cual la función está creando usuarios.

    :return: una lista de respuestas de una ejecución concurrente.
    """
    query = f''' EXEC sga.le_datos_matriculados '{semestre}' '''

    try:
        resultados = sql.lista_query(query)
        list_params = moodle.lista_concurr_usuarios(resultados)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            responses = list(executor.map(moodle.creacion_concurrente, list_params))

        return responses

    except requests.exceptions.RequestException as error:
        return f'Error en la creacion de usuarios, {error}'


# Nota (Lenin Elio - 29/04/2023 17:30)
# Busqueda e insersion de alumnos restantes
# Las funciones a continuacion estan creadas para la busqueda e insersion de alumnos
# que no llegaron a insertarse por el uso de funciones asincronas


def obtener_idusuario_username(username):
    """
    Esta función verifica si un usuario existe en Moodle por su nombre de usuario y devuelve
    su ID si existe.

    :param username: El nombre de usuario del usuario cuya ID necesita obtenerse.

    :return: Una tupla que contiene el nombre de usuario y Falso (si el usuario no existe
    en Moodle) o la ID del usuario (si el usuario existe en Moodle).
    """
    existe = moodle.async_idby_username(username)

    if existe['users'] == []:
        return (username, False)
    else:
        return (username, existe['users'][0]['id'])


def insertar_iduser_moodle_bd(alumnos):
    """
    Esta función inserta las ID de usuario de Moodle en una tabla de la base de datos y
    actualiza las ID correspondientes en otra tabla.

    :param alumnos: Es una lista de tuplas que contienen el nombre del estudiante y su
    correspondiente ID de Moodle

    :return: un mensaje de cadena que indica que se ha completado el proceso de inserción de las
    identificaciones de los estudiantes.
    """
    sql.ejecutar("CREATE TABLE sva.le_alumnos (nombreusuario VARCHAR(20), moodle_id INT)")

    query = 'INSERT INTO sva.le_alumnos (nombreusuario, moodle_id) VALUES (%d, %d)'
    sql.insertar_muchos(query, alumnos)

    sql.ejecutar("""
        UPDATE a
        SET a.moodle_id = la.moodle_id
        FROM dbo.Alumno as a
        INNER JOIN sva.le_alumnos as la
        ON a.Alumno = la.nombreusuario
    """)

    sql.ejecutar("DROP TABLE IF EXISTS sva.le_alumnos")

    return 'Subproceso: IDs de alumnos insertados.'


def insertar_iddocente_moodle_bd(docentes):
    """
    Insertar docente en la DB
    """
    sql.ejecutar("CREATE TABLE sva.le_docentes (nombreusuario VARCHAR(20), moodle_id INT)")

    for docente in docentes:
        data = {'nombreusuario': docente[0], 'moodle_id': docente[1]}
        sql.insertar_datos('sva.le_docentes', data)

    sql.ejecutar("""
        UPDATE t
        SET t.moodle_id = ld.moodle_id
        FROM dbo.Trabajador as t
        INNER JOIN sva.le_docentes as ld
        ON t.Dni = ld.nombreusuario
    """)

    sql.ejecutar("DROP TABLE IF EXISTS sva.le_docentes")

    return 'Subproceso: IDs de docentes insertados.'


def crear_docente_restante(lista):
    """
    Crear docente restante
    """
    docentes = "', '".join(lista)

    query = f'''
    SELECT LOWER
        (t.Dni) AS username,
        TRIM(t.Password) AS password,
        t.Nombre AS nombre,
        CONCAT ( t.ApellidoPaterno, ' ', t.ApellidoMaterno ) AS apellido,
        t.Email AS correo
    FROM
        dbo.Trabajador AS t
    WHERE
        t.Dni IN ('{docentes}')
    '''

    resultados = sql.lista_query(query)

    try:
        list_params = moodle.lista_concurr_usuarios(resultados)

        with ThreadPoolExecutor() as executor:
            problemas = list(executor.map(moodle.creacion_concurrente, list_params))

        if 'exception' in problemas:
            print(problemas)

        return 'Subproceso: Docentes restantes creados.'

    except requests.exceptions.RequestException as error:
        return f'Subproceso: Error en la creacion de docentes restantes, {error}'


def crear_usuario_restante(lista):
    """
    Esta función crea usuarios restantes consultando una base de datos y usando un ejecutor de
    grupo de subprocesos para crear usuarios simultáneamente en Moodle.

    :param lista: El parámetro "lista" es una lista de nombres de usuario para los cuales la
    función creará cuentas en Moodle

    :return: un mensaje de cadena que indica si el proceso de creación de usuarios restantes
    fue exitoso o si hubo un error.
    """
    usuarios = "', '".join(lista)

    query = f'''
    SELECT LOWER(Alumno) AS username,
    TRIM ( Password ) AS password,
    Nombre AS nombre,
    CONCAT ( ApellidoPaterno, ' ', ApellidoMaterno ) AS apellido,
    trim(Concat('temp_', Email)) as email 
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

    except requests.exceptions.RequestException as error:
        return f'Subproceso: Error en la creacion de usuarios restantes, {error}'


# Esta funcion en conjunto con sus subprocesos corrige a los alumnos no insertados por algun motivo
@decorador.calcular_tiempo_arg
def corregir_alumno_noinsertado(semestre):
    """
    Corregir la creacion de usuarios.
    """
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

        return 'No hay mas datos a corregir.'

    except requests.exceptions.RequestException as error:
        return f'Error en la correccion de alumnos, error: {error}'


def listar_docente_curso(cursos):
    """
    Obtener la lista de matriculados
    """
    with ThreadPoolExecutor() as executor:
        futures = [
              executor.submit(moodle.obtener_docente_matriculado, curso)
              for curso in cursos
        ]
        resultados = wait(futures)

    resultado_final = []
    for future in resultados.done:
        try:
            docentes = future.result()
            resultado_final.extend(docentes)

        except Exception as e_e: # pylint: disable=broad-except
            print(f"Ocurrió un error al obtener los matriculados del curso: {e_e}")

    return resultado_final


@decorador.calcular_tiempo_arg
def corregir_docente_noinsertado(semestre):
    """
    Corregir docente no insertado.
    """
    cursos_id = f'''
    SELECT lc.id_moodle 
    FROM sva.le_cursos lc 
    WHERE
        lc.semestre = '{semestre}'
        AND lc.docente_id IS NOT NULL
    '''
    cursos = sql.lista_query_especifico(cursos_id)
    cursos_moodle = listar_docente_curso(cursos)

    curso_docente = f'''
    SELECT
        lc.id_moodle, lc.docente_id 
    FROM
        sva.le_cursos lc 
    WHERE
        lc.semestre = '{semestre}'
        AND lc.docente_id IS NOT NULL
    '''

    cursos_sga = sql.lista_query(curso_docente)
    try:
        cursos_sga = set(cursos_sga)
        cursos_moodle = set(cursos_moodle)
        return (len(cursos_sga), len(cursos_moodle)), cursos_sga - cursos_moodle

    except requests.exceptions.RequestException as error:
        return f'Error en la comparacion, error: {error}'


@decorador.calcular_tiempo_arg
def creacion_docente_moodle(semestre):
    """
    Manejo de docentes
    """
    query = f'''
    SELECT DISTINCT 
        TRIM(t.Dni) AS dni 
    FROM
        dbo.CursoProgramado AS c
        INNER JOIN dbo.Trabajador AS t ON c.Trabajador = t.Trabajador 
    WHERE
        c.Semestre = '{semestre}' 
        AND t.Dni <> '' 
        AND t.moodle_id IS NULL 
        AND t.NombreCompleto NOT LIKE '%CONTRATO%' 
    '''

    resultados = sql.lista_query_especifico(query)

    try:
        if resultados != []:
            with ThreadPoolExecutor() as executor:
                results = list(executor.map(obtener_idusuario_username, resultados))

            existe = [(username, exists) for username, exists in results if exists > 0]
            noexiste = [username for username, exists in results if not exists]

            insertar_iddocente_moodle_bd(existe)
            crear_docente_restante(noexiste)

            return f'Docentes pendientes por insertar: {len(noexiste)}'

        return 'No hay mas datos a corregir.'

    except requests.exceptions.RequestException as error:
        return f'Error en la correccion de alumnos, error: {error}'

# Nota (Lenin Elio - 29/04/2023 17:39)
# Fin de busqueda e insersion de alumnos


# matricular estudiantes
@decorador.calcular_tiempo_arg
def matricular_usuarios(semestre, alumno=None):
    """
    Esta función matricula a los usuarios para un semestre determinado y, opcionalmente, para un
    estudiante específico.

    :param semestre: El semestre para el cual se están inscribiendo los usuarios.

    :param alumno: El parámetro "alumno" es un parámetro opcional que representa al alumno
    específico que se inscribirá en el curso.

    :return: un mensaje de cadena que dice "Matrículas realizadas con éxito". si el proceso
    de matriculación fue exitoso, "No hay matriculas a realizar". si no hay matrículas a
    realizar, o un mensaje de error si hubo un error durante el proceso de matrícula.
    """
    if alumno is None:
        query = f''' EXEC sga.le_matriculados '{semestre}' '''

    else:
        query = f''' EXEC sga.le_matriculados '{semestre}', '{alumno}' '''

    resultados = sql.lista_query(query)

    try:
        if resultados != []:

            list_params = moodle.concurr_matricular_usuario(resultados)

            with ThreadPoolExecutor() as executor:
                executor.map(moodle.creacion_concurrente, list_params)
                # responses = list(executor.map(moodle.creacion_concurrente, list_params))

            return 'Matriculas realizadas con exito.'

        return 'No hay matriculas a realizar.'

    except requests.exceptions.RequestException as error:
        return f'Error en las matriculas, error: {error}'


# matricular docentes
@decorador.calcular_tiempo_arg
def matricular_docentes(semestre, docente=None):
    """
    Matricular docentes.
    """
    if docente is None:
        query = f'''
        SELECT
            lc.id_moodle,
            lc.docente_id 
        FROM
            sva.le_cursos lc 
        WHERE
            lc.semestre = '{semestre}' 
            AND lc.docente_id IS NOT NULL
        '''

    else:
        query = f''' EXEC lx_matriculados '{semestre}', '{docente}' '''

    resultados = sql.lista_query(query)

    try:
        if resultados != []:

            list_params = moodle.concurr_matricular_usuario(resultados, 3)

            with ThreadPoolExecutor() as executor:
                executor.map(moodle.creacion_concurrente, list_params)

            return 'Matriculas de docentes realizadas con exito.'

        return 'No hay matriculas a realizar.'

    except requests.exceptions.RequestException as error:
        return f'Error en las matriculas, error: {error}'


# Nota (Lenin Elio - 29/04/2023 21:50)
# Busqueda e insersion de matriculas
# Las funciones a continuacion estan creadas para obtener las matriculas
# desde moodle y luego hacer la insercion en la base de datos
# esto con el fin de conocer que matriculas no se ejecutaron


def insertar_matriculas_bd():
    """
    Bulk SQL.
    """
    archivo = os.path.join(os.path.dirname(__file__), '../data/matriculas.csv')

    with sql.obtener_cursor() as cursor:
        cursor.execute(
            f'''
            BULK INSERT sva.le_matriculas_moodle
            FROM '{archivo}'
            WITH
                (
                    FIRSTROW = 2,
                    FIELDTERMINATOR = ',',
                    ROWTERMINATOR = '\n'
                )

            '''
            )

    return 'Se completo la insersion de datos obtenidos.'


def transformar_dataframe(dataframe):
    """
    La función transforma un marco de datos dado al extraer los valores de 'id' de ciertas columnas
    y los devuelve como una lista de tuplas.

    :param dataframe: un marco de datos de pandas que contiene columnas con información sobre
    los cursos inscritos y las identificaciones de los estudiantes

    :return: una lista de tuplas, donde cada tupla contiene dos elementos: la identificación de
    un curso y la identificación de un estudiante que está inscrito en ese curso.
    """
    obtenidos = []
    for col in dataframe.columns:
        for row in dataframe[col]:
            if row is not None and 'id' in row:
                cursos = [
                    curso['id']
                    for curso in row['enrolledcourses']
                    if 'id' in curso
                    ] if row['enrolledcourses'] is not None else []
                obtenidos.append([(curso, row['id']) for curso in cursos])

    obtenido = [ids for lista in obtenidos for ids in lista]
    return obtenido


@decorador.calcular_tiempo_arg
def obtener_matriculas_moodle_pandas(semestre):
    """
    Esta función obtiene los ID de los cursos de Moodle para un semestre determinado, los usa
    para realizar solicitudes asincrónicas a la API de Moodle, transforma los datos resultantes
    en un marco de datos de Pandas e inserta los datos en una base de datos.

    :param semestre: El parámetro "semestre" es una cadena que representa el semestre académico
    para el cual queremos obtener las inscripciones de Moodle.

    :return: un mensaje de cadena que indica el número de matriculas (inscripciones) que se
    han procesado o un mensaje de error si hubo un problema con el procesamiento.
    """
    semestre_val = sql.informacion_semestre(semestre)
    query = f"SELECT lc.id_moodle from sva.le_cursos lc where lc.semestre = '{semestre}'"

    cursos = sql.lista_query_especifico(query)

    try:
        if cursos != []:
            list_params = moodle.async_peticion_por_idcurso(cursos)

            with ThreadPoolExecutor() as executor:
                responses = list(executor.map(moodle.creacion_concurrente, list_params))

            json_data = json.dumps(responses)
            dataframe = pd.read_json(json_data)

            total_dados = transformar_dataframe(dataframe)
            matriculas = [matricula + (semestre_val[0], ) for matricula in total_dados]

            matriculas = set(matriculas)
            print(f'Subprocesando {len(matriculas)} matriculas.')

            query = '''
            INSERT INTO sva.le_matriculas_moodle 
            (curso_id, alumno_id, semestre_id) 
            VALUES (%d, %d, %d)
            '''
            sql.insertar_muchos(query, matriculas)

            return f'Se ha procesado {len(matriculas)} matriculas.'

        return 'Parece que hay un error en el semestre.'

    except requests.exceptions.RequestException as error:
        return f'Error en el procesado de matriculas con pandas, {error}'


# Nota (Lenin Elio - 29/04/2023 21:55)
# Fin de busqueda e insersion de matriculas


@decorador.calcular_tiempo_arg
def ocultar_cursos_moodle(semestre, lista=False):
    """
    Esta función oculta los cursos de Moodle para un semestre determinado.

    :param semestre: Una cadena que representa el semestre para el cual los cursos deben ocultarse.

    :param lista: Un parámetro booleano que indica si el parámetro semestre es una lista de ID de
    curso o una cadena que representa un semestre.

    :return: ya sea una cadena que indica que los cursos se ocultaron con éxito o que no hay
    más cursos para ocultar.
    """
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

        return 'No hay mas cursos por ocultar.'

    except requests.exceptions.RequestException as error:
        return f'Error al finalizar el semestre, error: {error}'


@decorador.calcular_tiempo_arg
def obtener_visibilidad_curso(semestre):
    """
    Esta función obtiene la visibilidad de los cursos de un semestre dado y oculta a los mismos.

    :param semestre: El semestre para el que se necesita obtener la visibilidad de los cursos.

    :return: una cadena que indica la cantidad de cursos que aún son visibles después de un
    proceso de obtención de visibilidad para los cursos. Si no hay más cursos para procesar,
    devuelve un mensaje indicándolo. Si hay un error en el proceso, devuelve un mensaje de error.
    """
    query = f"SELECT lc.id_moodle from sva.le_cursos lc WHERE lc.semestre = '{semestre}'"

    cursos = sql.lista_query_especifico(query)
    try:
        if cursos != []:

            list_params = moodle.listar_cursos_por_idcurso(cursos)

            with ThreadPoolExecutor() as executor:
                respuestas = list(executor.map(moodle.creacion_concurrente, list_params))

            visibles = [
                resp['courses'][0]['id']
                for resp in respuestas if resp['courses'] != []
                if resp['courses'][0]['visible'] == 1
                ]

            ocultar_cursos_moodle(visibles, True)

            return f'Cantidad de cursos que aun estan visibles: {len(visibles)}'
        return 'No hay mas cursos para procesar.'

    except requests.exceptions.RequestException as error:
        return f'Error en la obtencion de la visibilidad de cursos, error {error}'


@decorador.calcular_tiempo_arg
def desmatricular_usuario_username(semestre, username):
    """
    Esta función da de baja a un usuario de sus cursos en Moodle utilizando su nombre de usuario.

    :param username: El nombre de usuario del estudiante que necesita ser dado de baja de sus cursos

    :return: ya sea una cadena "Creo que no existe ese alumno" si el alumno no existe en la base de
    datos, o una lista de respuestas de un proceso simultáneo de cancelación de la inscripción del
    alumno en sus cursos en Moodle. Si hay un error con las solicitudes realizadas durante el
    proceso concurrente, la función devolverá el mensaje de error.
    """
    query = f'''SELECT moodle_id FROM dbo.Alumno WHERE '{semestre}' AND Alumno='{username}' '''
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
        return f'Ocurrio un error al desmatricular a un estudiante, error: {error}'


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
