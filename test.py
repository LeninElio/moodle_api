from functions import sql

# query = 'SELECT * FROM sva.le_semestre'
# data = sql.lista_query(query)

# print(data)


data = {'nombre': 'semestre', 'nombre_completo': 'name', 'descripcion': 'desc', 'parent': 13}

# insertar = sql.insertar_datos('sva.le_semestre', data)
insertar = sql.informacion_semestre('semestre')
print(insertar)

