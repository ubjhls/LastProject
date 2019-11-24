```python
from django.shortcuts import render,redirect,get_object_or_404
from .models import Movie, Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import requests
from .models import Movie,Genre
from django.core import serializers
import pprint

def genres_data():
    genres_url = 'https://api.themoviedb.org/3/genre/movie/list?api_key=f115f7077bf79f6f7fd3227c5ba7f281&language=ko-KR'
    response = requests.get(genres_url).json().get('genres')
    for r in response:
        genre = Genre(**r)
        genre.save()

def movies_data(page_num):
    movies_url = f'https://api.themoviedb.org/3/movie/top_rated?api_key=f115f7077bf79f6f7fd3227c5ba7f281&language=ko-KR&page={page_num}&region=KR'
    response = requests.get(movies_url).json().get('results')
    print('총 ' ,len(response) , '개')
    tmp = 0
    for r in response:
        id = r.get('id')
        if not Movie.objects.filter(pk=id):
            tmp += 1
            detail_url = f'https://api.themoviedb.org/3/movie/{id}?api_key=f115f7077bf79f6f7fd3227c5ba7f281&language=ko-KR'
            detail = requests.get(detail_url).json()
            
            movie = Movie.objects.create(
                adult = detail.get('adult'),
                backdrop_path = detail.get('backdrop_path'),
                budget = detail.get('budget'),
                id = detail.get('id'),
                original_language = detail.get('original_language'),
                overview = detail.get('overview'),
                popularity = detail.get('popularity'),
                poster_path = detail.get('poster_path'),
                release_date = detail.get('release_date'),
                revenue = detail.get('revenue'),
                runtime = detail.get('runtime'),
                status = detail.get('status'),
                tagline = detail.get('tagline'),
                title = detail.get('title'),
                video = detail.get('video'),
                vote_average = detail.get('vote_average'),
                vote_count = detail.get('vote_count')
            )
            for r in detail.get('genres'):
                genre = Genre.objects.get(pk=r.get('id'))
                movie.genres.add(genre)
            movie.save()
    print('등록 ',tmp , '개')

```

