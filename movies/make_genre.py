import requests
import json
import pprint

# movie
# url = 'https://api.themoviedb.org/3/genre/movie/list?api_key=1dfd52c8a24a0f38f40efe41c86be13b&language=ko-KR'
# tv
url = 'https://api.themoviedb.org/3/genre/tv/list?api_key=1dfd52c8a24a0f38f40efe41c86be13b&language=ko-KR'
response = requests.get(url).json()
pprint.pprint(response['genres'])
genre_info = []

for genre in response['genres']:
    new_genre = {
        'pk': genre['id'],
        'model': "movies.genre",
        'fields': {
            'name': genre['name']
        }
    }
    genre_info.append(new_genre)
pprint.pprint(genre_info)

with open('movies/fixtures/tv_genre.json', 'w', encoding='utf-8') as f:
    json.dump(genre_info, f, ensure_ascii=False, indent="\t")