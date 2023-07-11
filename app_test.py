from concurrent.futures import ThreadPoolExecutor
import json
import requests
import pandas as pd
from funciones import decorador, moodle, sql
from funciones import migracion as mg


@decorador.calcular_tiempo_arg
def obtener_matriculas_moodle_pandas(semestre):
    """
    Pruebas.
    """
    semestre_val = sql.informacion_semestre(semestre)
    cursos = ['8799', '10209', '12273', '11356', '13002', '13562', '10211', '8797', '8798', '11357']
    # cursos = ['8799']

    try:
        if cursos:
            list_params = moodle.async_peticion_por_idcurso(cursos)

            with ThreadPoolExecutor() as executor:
                responses = list(executor.map(moodle.creacion_concurrente, list_params))

            json_data = json.dumps(responses)
            dataframe = pd.read_json(json_data)

            total_datos = mg.transformar_dataframe(dataframe)
            matriculas = [matricula + (semestre_val[0], ) for matricula in total_datos]

            matriculas = set(matriculas)
            print(f'Subprocesando {len(matriculas)} matriculas.')

            # query = '''
            # INSERT INTO sva.le_matriculas_moodle
            # (curso_id, alumno_id, semestre_id)
            # VALUES (%d, %d, %d)
            # '''
            # sql.insertar_muchos(query, matriculas)

            matriculas = pd.DataFrame(matriculas, columns=['id_curso', 'id_usuario', 'semestre'])
            matriculas['semestre'] = semestre_val[0]
            matriculas.to_csv('./data/matriculas.csv', index=False)

            # mg.insertar_matriculas_bd(matriculas)

            return f'Se ha procesado {len(total_datos)} matriculas.'

        return 'Parece que hay un error en el semestre.'

    except requests.exceptions.RequestException as error:
        return f'Error en el procesado de matriculas con pandas, {error}'


# data = obtener_matriculas_moodle_pandas('2023-1')
# print(data)

data_insert = obtener_matriculas_moodle_pandas('2023-1')
print(data_insert)
