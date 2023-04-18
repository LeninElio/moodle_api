from funciones import moodle, sql
import concurrent.futures

# Semestre a crear
semestre = '2020-1'

# Creacion de la categoria principal
def crear_cat_semestre():

    try:
        name = f'Semestre {semestre}'  
        desc = f'Categoría para el semestre académico {semestre}'

        principal = moodle.crear_categoria(name, semestre, desc)
        data = {'nombre': semestre, 'nombre_completo': name, 'descripcion': desc, 'parent': principal[0]['id']}
        sql.insertar_datos('sva.le_semestre', data)
        print(data)

    except Exception as e:
        return f'Fallaste {e}'


# Creacion de la sub categoria facultades
def crear_cat_facultades():
    query = f'''
    SELECT
        CONCAT('{semestre}', '-', f.Facultad) cat_num, 
        CONCAT('FACULTAD DE ', f.Descripcion) as cat_name,
        CONCAT('CATEGORIA DE LA FACULTAD DE ', f.Descripcion) as cat_desc,
        f.Facultad
    FROM
        dbo.Facultad AS f
    WHERE f.Activo = '1' '''

    semestre_val = sql.informacion_semestre(semestre)

    try:
        resultados = sql.lista_query(query)

        for resultado in resultados:
            num = resultado[0]
            name = resultado[1]
            desc = resultado[2]
            idfac = resultado[3]
            
            facultades = moodle.crear_sub_categoria(name, num, desc, semestre_val[1])
            data = {'semestre': semestre_val[0], 'numeracion': num, 'parent': facultades[0]['id'], "idfac": idfac}
            sql.insertar_datos('sva.le_facultad', data)
            print(data)

    except Exception as e:
        return f'Fallaste {e}'


# Creacion de la sub categoria escuelas
def crear_cat_escuelas():
    semestre_val = sql.informacion_semestre(semestre)

    # Se le agrega algunas cosas al query para que la informacion sea mas legible
    query = f'''
    SELECT
        e.Descripcion as cat_name,
        CONCAT(f.numeracion, '-', e.Escuela) as num,
        CONCAT('ESCUELA PROFESIONAL DE ', e.Descripcion) as cat_desc,
        f.parent as parent,
        e.Escuela
    FROM
        dbo.Escuela AS e
        INNER JOIN sva.le_facultad AS f ON e.Facultad = f.idfac
    where e.Activo = '1' AND f.semestre = '{semestre_val[0]}' 
    '''

    try:
        resultados = sql.lista_query(query)
        for resultado in resultados:
            name = resultado[0]
            num = resultado[1]
            desc = resultado[2]
            parent = resultado[3]
            idesc = resultado[4]

            escuelas = moodle.crear_sub_categoria(name, num, desc, parent)
            data = {'semestre': semestre_val[0], 'numeracion': num, 'parent': escuelas[0]['id'], "idesc": idesc}
            sql.insertar_datos('sva.le_escuela', data)
            print(data)

    except Exception as e:
        return f'Fallaste {e}'


# Creacion de la sub categoria ciclos
def crear_cat_ciclos():
    query = f'''
    SELECT
        cp.Escuela,
        c.Ciclo,
        le.parent,
        concat ( le.numeracion, '-', c.Ciclo ) AS numeracion 
    FROM
        dbo.CursoProgramado AS cp
        INNER JOIN dbo.Curso AS c ON c.Curso = cp.Curso 
        AND cp.Escuela = c.Escuela 
        AND cp.Curricula = c.Curricula
        INNER JOIN sva.le_escuela le ON le.idesc = cp.Escuela 
    WHERE
        cp.Semestre = '{semestre}' 
    GROUP BY
        cp.Escuela,
        c.Ciclo,
        le.parent,
        le.numeracion 
    '''

    try:
        resultados = sql.lista_query(query)
        for resultado in resultados:
            # print(resultado)
            ciclos = moodle.crear_sub_categoria(resultado[1], resultado[3], resultado[1], resultado[2])
            data = {'numeracion': resultado[3], 'parent': ciclos[0]['id'], "idescparent": resultado[2], "idciclo": resultado[1]}
            sql.insertar_datos('sva.le_ciclo', data)
            print(data)

    except Exception as e:
        return f'Fallaste {e}'


# Creacion de la sub categoria ciclos
def crear_cursos():
    query = f'''
    SELECT
        concat ( cp.Semestre, ', ', c.Nombre, ', ', e.Abreviatura, ', ', cp.Seccion ) AS nombrecompleto,
        concat ( c.Nombre, ', ', e.Abreviatura, ', ', cp.Semestre, ', ', cp.Seccion ) AS idcurso,
        lc.parent 
    FROM
        dbo.CursoProgramado AS cp
        INNER JOIN dbo.Curso AS c ON cp.Curricula = c.Curricula 
        AND cp.Curso = c.Curso 
        AND cp.Escuela = c.Escuela
        INNER JOIN sva.le_escuela AS le ON c.Escuela = le.idesc
        INNER JOIN sva.le_ciclo AS lc ON le.parent = lc.idescparent 
        AND c.Ciclo = lc.idciclo
        INNER JOIN dbo.Escuela AS e ON c.Escuela = e.Escuela 
    WHERE
        cp.Semestre = '{semestre}'
    '''
    
    try:
        resultados = sql.lista_query(query)
        list_params = moodle.lista_concurr_cursos(resultados)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            responses = list(executor.map(moodle.crear_concurr_cursos, list_params))

        return responses
    
    except Exception as e:
        return f'Fallaste {e}'
    

crear_cursos()
