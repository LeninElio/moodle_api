import sys
sys.path.append(".")
from funciones import sql

data = sql.lista_query('select top 100 * from dbo.Rendimiento')

print(data)