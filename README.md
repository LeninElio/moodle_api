# API Moodle

Usando la API de moodle en conjunto con una base de datos SQL Server.

## .data

Contiene las el codigo de las tablas usadas.

## .funciones

En esta carpeta se encuentran las funciones para el manejo de la API y interaccion con la BD.

## .conexion

Conexion a la base de datos.

# Importante
La mayoria de las funciones usan concurrent futures por el siguiente motivo:

> asyncio es una buena opción para tareas que involucran muchas solicitudes de red, mientras que concurrent.futures es una buena opción para tareas que involucran mucho procesamiento de datos o CPU.
