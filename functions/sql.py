from conexion import db

conn = db.connection()
cursor = conn.cursor()


# Insertar datos
def insertar_datos(table, data):
    columns = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
    cursor.execute(query, tuple(data.values()))
    conn.commit()


# retorna un listado de datos
def lista_query(query):
    cursor.execute(query)
    datos = cursor.fetchall()
    return [dato for dato in datos]


# retorna el id y parent del semestre actual 
def informacion_semestre(semestre):
    cursor.execute(f"select id, parent from sva.le_semestre where nombre = '{semestre}'")
    datos = cursor.fetchone()
    return datos

