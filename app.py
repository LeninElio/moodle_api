"""Importando la función `migracion` desde el módulo `funciones` y renombrándola como `mg`."""

from funciones import migracion as mg # pylint: disable=unused-import


def main(semestre, semestre_anterior=None):
    """
    Ejecutar la app principal
    Este código es el programa principal que ejecuta una serie de funciones desde un módulo
    llamado "funciones". Estas funciones están relacionadas con la migración de cursos y usuarios
    en una plataforma Moodle para un semestre específico. El código incluye varias llamadas a
    funciones comentadas que se pueden descomentar y ejecutar según las necesidades específicas
    del proceso de migración. La llamada de función final imprime las inscripciones de Moodle
    restantes para el semestre.
    """
    # Paso 1. Finalizar semestre anterior (ocultar los cursos de la visibilidad de estudiantes)
    # ocultar = mg.ocultar_cursos_moodle(SEMESTRE_ANTERIOR)
    # print(ocultar)

    # Paso 2. Verificar si aun hay cursos del semestre anterior
    # visibles = mg.obtener_visibilidad_curso(semetre_anterior)
    # print(visibles)

    # Paso 3. Creacion del semestre
    # semestre_creado = mg.crear_semestre(semestre)
    # print(semestre_creado)

    # Paso 4. Creacion del categoria facultades
    # facultades_creados = mg.crear_facultades(semestre)
    # print(facultades_creados)

    # Paso 5. Creacion del categoria escuelas
    # escuelas_creadas = mg.crear_escuelas(semestre)
    # print(escuelas_creadas)

    # Paso 6. Creacion del categoria ciclos
    # ciclos_creados = mg.crear_ciclos(semestre)
    # print(ciclos_creados)

    # Paso 7. Creacion de docentes
    # docente = mg.creacion_docente_moodle(semestre)
    # print(docente)

    # Paso 8. Migracion de cursos a nivel de base de datos
    # migrar = mg.migracion_cursos_bd(semestre, '2023-07-09')
    # print(migrar)

    # Paso 9. Creacion de cursos
    # cursos_creados = mg.crear_cursos(semestre)
    # print(cursos_creados)

    # Paso 10. Algunos cursos no se insertaron por la concurrencia
    # Realizar varias ejecuciones hasta que no retorne cursos
    # corregir = mg.corregir_cursos_noinsertados(semestre)
    # print(corregir)

    # Paso 11. Matricular docentes, esta funcion recibe dos parametros semestre y docente
    # matricular = mg.matricular_docentes(semestre)
    # print(matricular)

    # Paso 12. Algunos docentes no se insertaron por la concurrencia
    # corregir_docentes = mg.corregir_docente_noinsertado(semestre)
    # print(corregir_docentes)

    # Paso 13. Crear usuarios (alumnos)
    # crear_usuarios = mg.crear_usuarios(semestre)
    # print(crear_usuarios)

    # Paso 14. Algunos alumno no se insertaron por la concurrencia
    # corregir_alumnos = mg.corregir_alumno_noinsertado(semestre)
    # print(corregir_alumnos)

    # Paso 15. Matricular usuarios, esta funcion recibe dos parametros semestre y alumno
    # alumno es opcional, por si quiere hacer matriculas de un solo alumno
    # matricular = mg.matricular_usuarios(semestre)
    # print(matricular)

    # Paso 16. Probablemente algunas matriculas fallen, en este caso se hace una busqueda de esos
    matriculas_restante = mg.obtener_matriculas_moodle_pandas(semestre)
    print(matriculas_restante)

    return f'Semestre actual: {semestre},  semestre anterior: {semestre_anterior}'


if __name__ == "__main__":
    SEMESTRE = '2023-1'
    SEMESTRE_ANTERIOR = '2022-2'
    main(SEMESTRE, SEMESTRE_ANTERIOR)
