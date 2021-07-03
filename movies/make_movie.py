import requests
import json
import pprint

movie_list = []
movie_info = []

for page in range(1, 11):
    # now_playing
    # url = f'https://api.themoviedb.org/3/movie/now_playing?api_key=1dfd52c8a24a0f38f40efe41c86be13b&language=ko-KR&page={page}'
    # popular
    # url = f'https://api.themoviedb.org/3/movie/popular?api_key=1dfd52c8a24a0f38f40efe41c86be13b&language=ko-KR&page={page}'
    # top_rated
    url = f'https://api.themoviedb.org/3/movie/top_rated?api_key=1dfd52c8a24a0f38f40efe41c86be13b&language=ko-KR&page={page}'    
    response = requests.get(url).json()
    for movie in response["results"]:
        movie_list.append(movie["id"])

for movie in movie_list:
    url = f"https://api.themoviedb.org/3/movie/{movie}?api_key=1dfd52c8a24a0f38f40efe41c86be13b&language=ko-KR"
    response = requests.get(url).json()
    video_url = f"https://api.themoviedb.org/3/movie/{movie}/videos?api_key=1dfd52c8a24a0f38f40efe41c86be13b&language=ko-KR"
    video_response = requests.get(video_url).json()
    if len(video_response["results"]) > 0:
        video_link = f'https://www.youtube.com/watch?v={video_response["results"][0]["key"]}'
    else:
        video_link = 'https://www.youtube.com/'
        
    if len(response['genres']) > 0:
        genres = response['genres'][0]['id']
    else:
        genres = 18
    back_image = 'https://image.flaticon.com/icons/svg/20/20773.svg'
    if response['backdrop_path']:
        back_image = response['backdrop_path']
    runtime = 120
    if response['runtime']:
        runtime = response['runtime']
    print(response['id'])
    new_movie = {
        'pk': response['id'],
        'model': "movies.Movie",
        'fields': {
            'title': response['title'],
            'movie_type': 'top_rated',
            'poster_url': f"https://image.tmdb.org/t/p/w500{response['poster_path']}",
            'description': response['overview'],
            'genre_id': genres,
            'video_link': video_link,
            'popularity': response['popularity'],
            'vote_average': response['vote_average'],
            'back_image': back_image,
            'release_date': response['release_date'],
            'runtime': runtime,
            'tagline': response['tagline'],
        }
    }
    movie_info.append(new_movie)

# pprint.pprint(movie_info)
with open('movies/fixtures/top_rated2.json', 'w', encoding='utf-8') as f:
    json.dump(movie_info, f, ensure_ascii=False, indent="\t")
