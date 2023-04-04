from functions import moodle, sql

# Semestre a crear
semestre = '2022-4'

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

    semestre_val = sql.retorna_valores_semestre('sva.le_semestre', semestre)

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
    semestre_val = sql.retorna_valores_semestre('sva.le_semestre', semestre)

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
    
