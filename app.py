# Importando la función `migracion` desde el módulo `funciones` y renombrándola como `mg`.

from concurrent.futures import ThreadPoolExecutor
from funciones import migracion as mg # noqa
from funciones import moodle

SEMESTRE_ANTERIOR = '2019-1'
SEMESTRE = '2020-2'

"""
Ejecutar la app principal
Este código es el programa principal que ejecuta una serie de funciones desde un módulo
llamado "funciones". Estas funciones están relacionadas con la migración de cursos y usuarios
en una plataforma Moodle para un semestre específico. El código incluye varias llamadas a
funciones comentadas que se pueden descomentar y ejecutar según las necesidades específicas
del proceso de migración. La llamada de función final imprime las inscripciones de Moodle
restantes para el semestre.
"""

if __name__ == "__main__":
    pass
    # A. Finalizar semestre anterior (ocultar los cursos de la visibilidad de estudiantes)
    # ocultar = mg.ocultar_cursos_moodle(SEMESTRE_ANTERIOR)
    # print(ocultar)

    # B. Verificar si aun hay cursos del semestre anterior
    # visibles = mg.obtener_visibilidad_curso(SEMESTRE_ANTERIOR)
    # print(visibles)

    # 1. Creacion del semestre
    # semestre_creado = mg.crear_semestre(SEMESTRE)
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

    # 8.1. Probablemente algunas matriculas fallen, en este caso se hace una busqueda esos
    # matriculas_restante = mg.obtener_matriculas_moodle_pandas(SEMESTRE)
    # print(matriculas_restante)


def listar_tareas():
    """
    Obtener la lista de tareas
    """
    cursos = [9899, 9890]
    peticion = moodle.concurr_obtener_tareas(cursos)
    with ThreadPoolExecutor() as executor:
        responses = list(executor.map(moodle.creacion_concurrente, peticion))

    return [
        {curso['id']: [tarea['id'] for tarea in curso['assignments']]}
        for respuesta in responses if respuesta['courses'] != []
        for curso in respuesta['courses']
        ]


def listar_archivos():
    """
    Obtener la lista de archivos
    """
    cursos = [9899, 9890]
    peticion = moodle.concurr_obtener_archivos(cursos)
    with ThreadPoolExecutor() as executor:
        responses = list(executor.map(moodle.creacion_concurrente, peticion))

    return responses


archivos = listar_archivos()
print(archivos)
