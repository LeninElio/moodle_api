import requests
import concurrent.futures


url = 'https://rickandmortyapi.com/api/character/{}'


def obtener_nombre(personaje):
    response = requests.get(url.format(personaje))
    data = response.json()
    return data['name']


if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor() as executor:
        tareas = [executor.submit(obtener_nombre, personaje) for personaje in range(1, 10)]
        for tarea in concurrent.futures.as_completed(tareas):
            print(tarea.result())
