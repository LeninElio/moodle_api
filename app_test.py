from concurrent.futures import ThreadPoolExecutor
import requests
from funciones import decorador, moodle, sql


# matricular estudiantes
@decorador.calcular_tiempo_arg
def matricular_usuarios(semestre, alumno=None):
    """
    :return: un mensaje de cadena que dice "Matrículas realizadas con éxito". si el proceso
    de matriculación fue exitoso, "No hay matriculas a realizar". si no hay matrículas a
    realizar, o un mensaje de error si hubo un error durante el proceso de matrícula.
    """
    if alumno is None:
        query = f''' EXEC le_matriculados '{semestre}' '''

    else:
        query = f''' EXEC le_matriculados '{semestre}', '{alumno}' '''

    resultados = sql.lista_query(query)

    try:
        if resultados != []:

            list_params = moodle.concurr_matricular_usuario(resultados)

            print(list_params)
            # with ThreadPoolExecutor() as executor:
            #     executor.map(moodle.creacion_concurrente, list_params)

            return 'Matriculas realizadas con exito.'

        return 'No hay matriculas a realizar.'

    except requests.exceptions.RequestException as error:
        return f'Error en las matriculas, error: {error}'
