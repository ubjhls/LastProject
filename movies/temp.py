import requests
import json
import pprint

movie_list = []
movie_info = []


url = "https://api.themoviedb.org/3/movie/now_playing?page=1&language=ko-KR&api_key=1dfd52c8a24a0f38f40efe41c86be13b"
response = requests.get(url).json()
for movie in response["results"]:
    movie_list.append(movie["id"])



for movie in movie_list:
    url = f"https://api.themoviedb.org/3/movie/{movie}?api_key=1dfd52c8a24a0f38f40efe41c86be13b&language=ko-KR"
    response = requests.get(url).json()
    new_movie = {
        'pk': response['id'],
        'model': "movies.Movie",
        'fields': {
            'title': response['title'],
            'poster_url': f"https://image.tmdb.org/t/p/w500{response['poster_path']}",
            'description': response['overview'],
            'genre_id': response['genres']
        }
    }
    movie_info.append(new_movie)

pprint.pprint(movie_info)
with open('movies/fixtures/movie_list.json', 'w', encoding='utf-8') as f:
    json.dump(movie_info, f, ensure_ascii=False, indent="\t")
