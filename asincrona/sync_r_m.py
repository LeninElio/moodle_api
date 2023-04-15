import requests

url = 'https://rickandmortyapi.com/api/character/{}'

for personaje in range(1, 10):
    response = requests.get(url.format(personaje))
    data = response.json()
    print(data['name'])