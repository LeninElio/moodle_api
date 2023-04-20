from funciones import moodle, sql, principal
import concurrent.futures
import pandas as pd

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
            responses = list(executor.map(moodle.creacion_concurrente, list_params))

        return responses
    
    except Exception as e:
        return f'Fallaste {e}'
    

def crear_usuarios():
    query = f'''
    SELECT DISTINCT
        a.alumno,
        a.password,
        a.nombre,
        a.apellido,
        a.email
    FROM
        le_correolimpio AS a
    WHERE
        (a.email <> '' or a.email IS NULL)
        AND CHARINDEX('@', a.email) > 0
        AND CHARINDEX('.', a.email, CHARINDEX('@', a.email)) > 0
        AND CHARINDEX(' ', a.email) = 0
        AND PATINDEX('%[,"()<>;[]]%', a.email) = 0
    GROUP BY
        a.email,
    a.alumno,
        a.password,
        a.nombre,
        a.apellido
    '''

    try:
        resultados = sql.lista_query(query)
        list_params = moodle.lista_concurr_usuarios(resultados)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            responses = list(executor.map(moodle.creacion_concurrente, list_params))

        return responses
    
    except Exception as e:
        return f'Fallaste {e}'


def matricular_alumnos(func):
    def ejecutor():
        try:
            matriculados = func()
            lista_matriculados = moodle.lista_concurr_matriculas(matriculados)
            with concurrent.futures.ThreadPoolExecutor() as executor:
                responses = list(executor.map(moodle.creacion_concurrente, lista_matriculados))

            return responses
        
        except Exception as e:
            return f'Fallaste en matricular_alumnos {e}'
    return ejecutor
    

# @matricular_alumnos
@principal.calcular_tiempo
def obtener_alumnos_cursos():
    query = f'''
    SELECT TOP 1000
        LOWER(r.Alumno) AS alumno,
        concat ( c.Nombre, ', ', e.Abreviatura, ', ', cp.Semestre, ', ', cp.Seccion ) AS idcurso 
    FROM
        dbo.Rendimiento AS r
        INNER JOIN dbo.Curso AS c ON r.Curricula = c.Curricula 
        AND r.Curso = c.Curso 
        AND r.Escuela = c.Escuela
        INNER JOIN dbo.CursoProgramado AS cp ON c.Curricula = cp.Curricula 
        AND c.Curso = cp.Curso 
        AND c.Escuela = cp.Escuela 
        AND r.Semestre = cp.Semestre 
        AND r.Seccion = cp.Seccion
        INNER JOIN dbo.Escuela AS e ON cp.Escuela = e.Escuela 
    WHERE
        r.Semestre = '2020-1';
    '''

    # try:

    resultados = sql.lista_query(query)
    lista_cursos = moodle.lista_concurr_byshortname(resultados)
    lista_alumnos = moodle.lista_concurr_byusername(resultados)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        cursos = list(executor.map(moodle.creacion_concurrente, lista_cursos))
        alumnos = list(executor.map(moodle.creacion_concurrente, lista_alumnos))

    with open("./test_data/temp_data.txt", "a", encoding='utf-8') as file:
        for matricula in zip(alumnos, cursos):
            # matriculados = f"{matricula[0]['users'][0]['id']}, {matricula[1]['courses'][0]['id']}"
            file.write(str(matricula) + "\n")
    
    # except Exception as e:
    #     return f'Fallaste {e}'


obtener_alumnos_cursos()

# @principal.calcular_tiempo
# def conwith():
#     with open('./test_data/temp_data.txt', 'r', encoding='utf-8') as file:
#         datos = file.readlines()
#         resultados = [[int(x) for x in dato.split(',')] for dato in datos]
    
#     return resultados

# # print(resultado)



# @principal.calcular_tiempo
# def pandita():
#     df = pd.read_csv('./test_data/temp_data.txt', header=None, names=['A', 'B'])
#     lista = df.values.tolist()
#     return lista


# conwith()

# pandita()
