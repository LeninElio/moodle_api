from funciones import moodle, sql, principal
import concurrent.futures
import pandas as pd

# @principal.calcular_tiempo

def listar_matriculados(semestre):
    # query = f'''
    # SELECT DISTINCT TOP 10 LOWER
    #     (r.Alumno) AS alumno 
    # FROM
    #     Rendimiento r 
    # WHERE
    #     r.Semestre = '{semestre}'
    # '''
    
    # resultados = sql.lista_query_especifico(query)
    resultados = ['131.2502.153', '00.0018.n.ac', '00.0360.1.ad', '00.0496.5.ao', '00.0600.n.ad', '01.0147.6.dl', '01.0227.9.ah', '01.0234.8.an', '01.0284.1.eo', '02.0276.2.de', '02.0391.3.ar']
    noexiste = []
    for resultado in resultados:
        existe = moodle.iduser_por_usernamex(resultado)
        if existe['users'] == []:
            noexiste.append(resultado)
        else:
            pass
    
    print(noexiste)
    

def listar_matriculado(semestre):
    # query = f'''
    # SELECT DISTINCT TOP 10 LOWER
    #     (r.Alumno) AS alumno 
    # FROM
    #     Rendimiento r 
    # WHERE
    #     r.Semestre = '{semestre}'
    # '''
    
    # resultados = sql.lista_query_especifico(query)
    resultados = ['131.2502.153', '00.0018.n.ac', '00.0360.1.ad', '00.0496.5.ao', '00.0600.n.ad', '01.0147.6.dl', '01.0227.9.ah', '01.0234.8.an', '01.0284.1.eo', '02.0276.2.de', '02.0391.3.ar']
    
    # noexiste = []
    # for resultado in resultados:
    #     existe = moodle.iduser_por_usernamex(resultado)
    #     if existe['users'] == []:
    #         noexiste.append(resultado)
    #     else:
    #         pass
    
    # print(noexiste)

    lista_alumnos = moodle.lista_concurr_byusernamex(resultados)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        alumnos = list(executor.map(moodle.creacion_concurrente, lista_alumnos))
        print(alumnos)
    

listar_matriculado('2020-1')


# listar_matriculados('2020-1')