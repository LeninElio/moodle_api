from funciones import migracion as mg


semestre = '2019-2'


if __name__ == "__main__":

    # 1. Creacion del semestre
    # semestre_creado = mg.crear_semestre(semestre)
    # print(semestre_creado)
    
    # 2. Creacion del categoria facultades
    # facultades_creados = mg.crear_facultades(semestre)
    # print(facultades_creados)

    # 3. Creacion del categoria escuelas
    # escuelas_creadas = mg.crear_escuelas(semestre)
    # print(escuelas_creadas)

    # 4. Creacion del categoria ciclos
    # ciclos_creados = mg.crear_ciclos(semestre)
    # print(ciclos_creados)

    # 5. Migracion de cursos a nivel de base de datos
    # migracion = mg.migracion_cursos_bd('2019-2', '2023-04-30')
    # print(migracion)

    # 6. Creacion de cursos
    # cursos_creados = mg.crear_cursos(semestre)
    # print(cursos_creados)

    # 6.1. Algunos cursos no se insertaron por la concurrencia
    #      Realizar varias ejecuciones hasta que no retorne cursos
    # corregir = mg.corregir_cursos_noinsertados(semestre)
    # print(corregir)

    # 7. Crear usuarios (alumnos), usar la opcion si no tiene alumnos creados en moodle
    # crear_usuarios = mg.crear_usuarios(semestre)
    # print(crear_usuarios)
    
    # 7.1. Algunos alumno no se insertaron por la concurrencia
    # corregir_alumnos = mg.corregir_alumno_noinsertado(semestre)
    # print(corregir_alumnos)

    # 8. Matricular usuarios, esta funcion recibe dos parametros semestre, alumno
    # alumno es opcionar
    # matricular = mg.matricular_usuarios(semestre)
    # print(matricular)

    # Probablemente algunas matriculas fallen, en este caso se hace una busqueda esos
    matriculas_restante = mg.obtener_matriculas_moodle_pandas(semestre)
    print(matriculas_restante)
    





