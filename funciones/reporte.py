from concurrent.futures import ThreadPoolExecutor, wait
from collections import defaultdict
from datetime import datetime
import pandas as pd
from funciones import moodle, decorador

def descargar_xlsx(respuesta):
    """
    Descargar el archivo xlsx de un dataframe
    """
    actual = datetime.now()
    actual = f'{actual:%Y-%m-%d %H%M}'
    data_frame = pd.DataFrame(respuesta)
    data_frame.to_excel(f'./data/notas_{actual}.xlsx', index=False)
    return 'Descarga completa.'


@decorador.calcular_tiempo_arg
def listar_contenido_cursos_semana(cursos):
    """
    Obtener la lista de todo el contenido del curso de forma concurrente
    mejorado la peticion para identificar cursos y todos los recursos
    """
    with ThreadPoolExecutor() as executor:
        futures = [
              executor.submit(moodle.obtener_todos_recursos_semana, curso)
              for curso in cursos
        ]
        resultados = wait(futures)

    resultado_final = {}
    for future in resultados.done:
        try:
            resultado = future.result()
            resultado_final.update(resultado)

        except Exception as e_e: # pylint: disable=broad-except
            print(f"Ocurrió un error al obtener los recursos del curso: {e_e}")

    return resultado_final


# cursos_id = [8611]
# contenidos = listar_contenido_cursos_semana(cursos_id)
# print(json.dumps(contenidos))


@decorador.calcular_tiempo_arg
def listar_notas_curso(curso):
    """
    Obtener todas las notas del curso en un archivo excel
    """
    contenido = moodle.obtener_notas_curso(curso)

    data = []
    for conten in contenido['usergrades']:
        for grade in conten['gradeitems']:
            if grade['grademax'] == 20:
                data.append((conten['userfullname'], grade['itemname'], grade['gradeformatted']))

    respuesta = defaultdict(list)
    for alumno, examen, nota in data:
        if alumno not in respuesta['alumno']:
            respuesta['alumno'].append(alumno)
        respuesta[examen].append(nota)

    descargar_xlsx(respuesta)


# CURSO_ID = 8611
# listar_notas_curso(CURSO_ID)
