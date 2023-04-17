import requests, os, time
from dotenv import load_dotenv

load_dotenv('private/.env')

api_key = os.getenv('API_KEY')
url = os.getenv('url')

global_params = {
    "wstoken": api_key,
    "moodlewsrestformat": "json"
}

resultados = [('01', 'I   ', 250, '2022-13-02-01-I   '), ('01', 'II  ', 250, '2022-13-02-01-II  '), ('01', 'III ', 250, '2022-13-02-01-III '), ('01', 'IX  ', 250, '2022-13-02-01-IX  '), ('01', 'V   ', 250, '2022-13-02-01-V   '), ('01', 'VI  ', 250, '2022-13-02-01-VI  '), ('01', 'VII ', 250, '2022-13-02-01-VII '), ('01', 'VIII', 250, '2022-13-02-01-VIII'), ('01', 'X   ', 250, '2022-13-02-01-X   '), ('02', 'I   ', 251, '2022-13-04-02-I   '), ('02', 'II  ', 251, '2022-13-04-02-II  '), ('02', 'III ', 251, '2022-13-04-02-III '), ('02', 'IV  ', 251, '2022-13-04-02-IV  '), ('02', 'IX  ', 251, '2022-13-04-02-IX  '), ('02', 'V   ', 251, '2022-13-04-02-V   '), ('02', 'VI  ', 251, '2022-13-04-02-VI  '), ('02', 'VII ', 251, '2022-13-04-02-VII '), ('02', 'VIII', 251, '2022-13-04-02-VIII'), ('02', 'X   ', 251, '2022-13-04-02-X   '), ('03', 'I   ', 252, '2022-13-02-03-I   '), ('03', 'II  ', 252, '2022-13-02-03-II  '), ('03', 'III ', 252, '2022-13-02-03-III '), ('03', 'IV  ', 252, '2022-13-02-03-IV  '), ('03', 'IX  ', 252, '2022-13-02-03-IX  '), ('03', 'V   ', 252, '2022-13-02-03-V   '), ('03', 'VI  ', 252, '2022-13-02-03-VI  '), ('03', 'VII ', 252, '2022-13-02-03-VII '), ('03', 'VIII', 252, '2022-13-02-03-VIII'), ('03', 'X   ', 252, '2022-13-02-03-X   '), ('04', 'I   ', 253, '2022-13-01-04-I   '), ('04', 'II  ', 253, '2022-13-01-04-II  '), ('04', 'III ', 253, '2022-13-01-04-III '), ('04', 'IV  ', 253, '2022-13-01-04-IV  '), ('04', 'IX  ', 253, '2022-13-01-04-IX  '), ('04', 'V   ', 253, '2022-13-01-04-V   '), ('04', 'VI  ', 253, '2022-13-01-04-VI  '), ('04', 'VII ', 253, '2022-13-01-04-VII '), ('04', 'VIII', 253, '2022-13-01-04-VIII'), ('04', 'X   ', 253, '2022-13-01-04-X   '), ('05', 'I   ', 254, '2022-13-01-05-I   '), ('05', 'II  ', 254, '2022-13-01-05-II  '), ('05', 'III ', 254, '2022-13-01-05-III '), ('05', 'IV  ', 254, '2022-13-01-05-IV  '), ('05', 'IX  ', 254, '2022-13-01-05-IX  '), ('05', 'V   ', 254, '2022-13-01-05-V   '), ('05', 'VII ', 254, '2022-13-01-05-VII '), ('05', 'X   ', 254, '2022-13-01-05-X   '), ('06', 'I   ', 255, '2022-13-05-06-I   '), ('06', 'III ', 255, '2022-13-05-06-III '), ('06', 'IV  ', 255, '2022-13-05-06-IV  '), ('06', 'IX  ', 255, '2022-13-05-06-IX  '), ('06', 'V   ', 255, '2022-13-05-06-V   '), ('06', 'VI  ', 255, '2022-13-05-06-VI  '), ('06', 'VII ', 255, '2022-13-05-06-VII '), ('06', 'VIII', 255, '2022-13-05-06-VIII'), ('06', 'X   ', 255, '2022-13-05-06-X   '), ('07', 'I   ', 256, '2022-13-05-07-I   ')]

session = requests.Session()

def crear_sub_categoria(params):
    response = session.post(f"{url}", params=params).json()
    return response

def crear_cat_ciclos():
    try:
        list_params = [{
            "wsfunction": "core_course_create_categories",
            "categories[0][name]": resultado[1],
            "categories[0][idnumber]": resultado[3],
            "categories[0][description]": resultado[1],
            "categories[0][parent]": resultado[2]
        } for resultado in resultados]

        params_list = [{**global_params, **params} for params in list_params]
        
        responses = list(map(crear_sub_categoria, params_list))
    
        return responses
    
    except Exception as e:
        return f'Fallaste {e}'


inicio = time.time()
crear_cat_ciclos()
fin = time.time()

print(f"Tiempo de ejecución: {fin - inicio} segundos")
