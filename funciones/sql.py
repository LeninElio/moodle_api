from conexion import db
from contextlib import contextmanager

# Funciones mejoradas
@contextmanager
def obtener_cursor():
    conn = db.connection()
    cursor = conn.cursor()
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


# Insertar datos
def insertar_datos(table, data):
    columns = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
    # cuando se usa context manager ya no es necesario usar conn.commit()
    with obtener_cursor() as cursor:
        cursor.execute(query, tuple(data.values()))


# Actualizar datos
def actualizar_datos(set_values, condition):
    # set_values = ', '.join([f"{key} = {value}" for key, value in data.items()])
    query = f"UPDATE dbo.Alumno SET moodle_id = {set_values} WHERE Alumno = %s"
    with obtener_cursor() as cursor:
        cursor.execute(query, condition)


def ejecutar(query):
    with obtener_cursor() as cursor:
        cursor.execute(query)


# retorna un listado de datos
def lista_query(query):
    with obtener_cursor() as cursor:
        cursor.execute(query)
        datos = cursor.fetchall()
    return [dato for dato in datos]


def lista_query_especifico(query):
    with obtener_cursor() as cursor:
        cursor.execute(query)
        datos = cursor.fetchall()
    return [dato[0] for dato in datos]


def lista_query_uno(query):
    with obtener_cursor() as cursor:
        cursor.execute(query)
        datos = cursor.fetchone()
    try:
        return datos[0]
    except TypeError:
        return None


# retorna el id y parent del semestre actual 
def informacion_semestre(semestre):
    with obtener_cursor() as cursor:
        cursor.execute(f"select id, parent from sva.le_semestre where nombre = '{semestre}'")
        datos = cursor.fetchone()
    return datos


# Funciones antiguas
# conn = db.connection()
# cursor = conn.cursor()


# # Insertar datos
# def insertar_datos(table, data):
#     columns = ', '.join(data.keys())
#     values = ', '.join(['%s'] * len(data))
#     query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
#     cursor.execute(query, tuple(data.values()))
#     conn.commit()


# # retorna un listado de datos
# def lista_query(query):
#     cursor.execute(query)
#     datos = cursor.fetchall()
#     return [dato for dato in datos]


# # retorna el id y parent del semestre actual 
# def informacion_semestre(semestre):
#     cursor.execute(f"select id, parent from sva.le_semestre where nombre = '{semestre}'")
#     datos = cursor.fetchone()
#     return datos

