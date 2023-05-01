""" Este módulo contiene funciones que interactuan con la base de datos """

from contextlib import contextmanager
from conexion import db


@contextmanager
def obtener_cursor():
    """
    Esta función devuelve un objeto de cursor para una conexión de base de datos 
    y maneja confirmaciones y reversiones de transacciones.
    :return: un mensaje de cadena que indica el estado de la transacción y la conexión.
    """
    conn = db.connection()
    cursor = conn.cursor()
    mensaje = ''
    try:
        yield cursor
        conn.commit()
        mensaje = "Transacción realizada con éxito."
    except:
        conn.rollback()
        mensaje = "La transacción ha fallado. Se ha realizado un rollback."
        raise
    finally:
        conn.close()
        mensaje += " Conexión cerrada."

    return mensaje


def insertar_datos(table, data):
    """
    Esta función inserta datos en una tabla específica en una base de datos
    mediante una consulta SQL.
    
    :param table: El nombre de la tabla donde se insertarán los datos
    :param data: Un diccionario que contiene los datos que se insertarán en la tabla. Las claves del
    diccionario representan los nombres de las columnas y los valores representan los valores que se
    insertarán en esas columnas
    """
    columns = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
    # cuando se usa context manager ya no es necesario usar conn.commit()
    with obtener_cursor() as cursor:
        cursor.execute(query, tuple(data.values()))


def actualizar_datos(set_values, condition):
    """
    Esta función actualiza el valor moodle_id en la tabla Alumno para una condición dada.
    
    :param set_values: El valor que se establecerá para la columna "moodle_id" 
    en la tabla "Alumno". Es una variable que debe contener el nuevo valor de la columna
    :param condition: El parámetro de condición es un marcador de posición para el valor 
    que se usará para filtrar las filas en la tabla del alumno que se actualizará. 
    Se utiliza en la cláusula WHERE de la consulta SQL para especificar la condición 
    que debe cumplirse para que se produzca la actualización
    """
    query = f"UPDATE dbo.Alumno SET moodle_id = {set_values} WHERE Alumno = %s"
    with obtener_cursor() as cursor:
        cursor.execute(query, condition)


def ejecutar(query):
    """
    Esta función ejecuta una consulta dada usando un cursor obtenido de otra función.
    
    :param query: El parámetro de consulta es una cadena que representa una consulta SQL que debe
    ejecutarse en una base de datos
    """
    with obtener_cursor() as cursor:
        cursor.execute(query)


def lista_query(query):
    """
    La función "lista_query" ejecuta una consulta SQL y devuelve los resultados en forma de lista.
    
    :param query: La consulta SQL que se ejecutará para recuperar datos de una base de datos
    :return: La función `lista_query` devuelve una lista de datos extraídos de la base de datos
    utilizando la consulta SQL proporcionada.
    """
    with obtener_cursor() as cursor:
        cursor.execute(query)
        datos = cursor.fetchall()
    return [dato for dato in datos]


def lista_query_especifico(query):
    """
    Esta función ejecuta una consulta específica y devuelve una lista del primer elemento de 
    cada fila de los datos resultantes.
    
    :param query: El parámetro de consulta es una cadena que representa una consulta SQL que se
    ejecutará en una base de datos
    :return: una lista del primer elemento de cada tupla en el conjunto de resultados obtenido al
    ejecutar la consulta SQL de entrada.
    """
    with obtener_cursor() as cursor:
        cursor.execute(query)
        datos = cursor.fetchall()
    return [dato[0] for dato in datos]


def lista_query_uno(query):
    """
    La función ejecuta una consulta SQL y devuelve el primer resultado como un valor único.
    
    :param query: El parámetro de consulta es una cadena que representa una consulta SQL que se va a
    ejecutar
    :return: La función `lista_query_uno` devuelve el primer elemento de la primera fila 
    del conjunto de resultados obtenido al ejecutar la entrada `query` utilizando un cursor 
    de base de datos. Si no hay un conjunto de resultados o el primer elemento es "Ninguno", 
    la función devuelve "Ninguno".
    """
    with obtener_cursor() as cursor:
        cursor.execute(query)
        datos = cursor.fetchone()
    try:
        return datos[0]
    except TypeError:
        return None


def informacion_semestre(semestre):
    """
    Esta función recupera el ID y el padre de un semestre de una base de datos según su nombre.
    
    :param semestre: El parámetro "semestre" es una cadena que representa el nombre 
    de un semestre. La función "informacion_semestre" recupera información sobre el 
    semestre de una tabla de base de datos llamada "sva.le_semestre" utilizando como 
    filtro el nombre del semestre proporcionado. La función devuelve una tupla que contiene el "id
    :return: una tupla con dos valores: el id y el padre de un semestre, obtenidos 
    de una consulta de base de datos basada en el parámetro de entrada "semestre".
    """
    with obtener_cursor() as cursor:
        cursor.execute(f"select id, parent from sva.le_semestre where nombre = '{semestre}'")
        datos = cursor.fetchone()
    return datos
