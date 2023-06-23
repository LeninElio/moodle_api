"""Importando la función `migracion` desde el módulo `funciones` y renombrándola como `mg`."""

from concurrent.futures import ThreadPoolExecutor, wait
import json
from collections import defaultdict
from funciones import migracion as mg
from funciones import moodle
from funciones import decorador
from funciones import reporte


def main(semestre, semetre_anterior):
    """
    Ejecutar la app principal
    Este código es el programa principal que ejecuta una serie de funciones desde un módulo
    llamado "funciones". Estas funciones están relacionadas con la migración de cursos y usuarios
    en una plataforma Moodle para un semestre específico. El código incluye varias llamadas a
    funciones comentadas que se pueden descomentar y ejecutar según las necesidades específicas
    del proceso de migración. La llamada de función final imprime las inscripciones de Moodle
    restantes para el semestre.
    """
    # A. Finalizar semestre anterior (ocultar los cursos de la visibilidad de estudiantes)
    # ocultar = mg.ocultar_cursos_moodle(SEMESTRE_ANTERIOR)
    # print(ocultar)

    # B. Verificar si aun hay cursos del semestre anterior
    # visibles = mg.obtener_visibilidad_curso(semetre_anterior)
    # print(visibles)

    # 1. Creacion del semestre
    # semestre_creado = mg.crear_semestre(semestre)
    # print(semestre_creado)

    # 2. Creacion del categoria facultades
    # facultades_creados = mg.crear_facultades(SEMESTRE)
    # print(facultades_creados)

    # 3. Creacion del categoria escuelas
    # escuelas_creadas = mg.crear_escuelas(SEMESTRE)
    # print(escuelas_creadas)

    # 4. Creacion del categoria ciclos
    # ciclos_creados = mg.crear_ciclos(SEMESTRE)
    # print(ciclos_creados)

    # 5. Migracion de cursos a nivel de base de datos
    # migrar = mg.migracion_cursos_bd(SEMESTRE, '2023-05-04')
    # print(migrar)

    # 6. Creacion de cursos
    # cursos_creados = mg.crear_cursos(SEMESTRE)
    # print(cursos_creados)

    # 6.1. Algunos cursos no se insertaron por la concurrencia
    #      Realizar varias ejecuciones hasta que no retorne cursos
    # corregir = mg.corregir_cursos_noinsertados(SEMESTRE)
    # print(corregir)

    # 7. Crear usuarios (alumnos), usar la opcion si no tiene alumnos creados en moodle
    # crear_usuarios = mg.crear_usuarios(SEMESTRE)
    # print(crear_usuarios)

    # 7.1. Algunos alumno no se insertaron por la concurrencia
    # corregir_alumnos = mg.corregir_alumno_noinsertado(SEMESTRE)
    # print(corregir_alumnos)

    # 8. Matricular usuarios, esta funcion recibe dos parametros semestre y alumno
    # alumno es opcional, por si quiere hacer matriculas de un solo alumno
    # matricular = mg.matricular_usuarios(SEMESTRE)
    # print(matricular)

    # 8.1. Probablemente algunas matriculas fallen, en este caso se hace una busqueda de esos
    # matriculas_restante = mg.obtener_matriculas_moodle_pandas(SEMESTRE)
    # print(matriculas_restante)

    return mg.crear_cursos('ret'), semestre, semetre_anterior


@decorador.calcular_tiempo_arg
def listar_contenido_cursos_semana(cursos):
    """
    Obtener la lista de todo el contenido del curso de forma concurrente
    mejorado la peticion para identificar cursos y todos los recursos
    """
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(moodle.obtener_todos_recursos_semana, curso) for curso in cursos]
        resultados = wait(futures)

    resultado_final = {}
    for future in resultados.done:
        try:
            resultado = future.result()
            resultado_final.update(resultado)

        except Exception as e_e: # pylint: disable=broad-except
            print(f"Ocurrió un error al obtener los recursos del curso: {e_e}")

    return resultado_final


cursos_id = [8611]
contenidos = listar_contenido_cursos_semana(cursos_id)
print(json.dumps(contenidos))


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

    reporte.descargar_xlsx(respuesta)


CURSO_ID = 8611
listar_notas_curso(CURSO_ID)


# if __name__ == "__main__":
#     SEMESTRE = '2020-2'
#     SEMESTRE_ANTERIOR = '2019-1'
#     main(SEMESTRE, SEMESTRE_ANTERIOR)
