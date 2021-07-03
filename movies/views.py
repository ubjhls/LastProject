from django.shortcuts import render,redirect,get_object_or_404
from .models import Movie, Genre, Review
from .forms import ReviewForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden,HttpResponse,JsonResponse
import requests
from django.core import serializers
import pprint
from django.db.models import Avg, Max, Min, Sum
from django.contrib.auth import get_user_model
import json
from django.contrib import messages

# Create your views here.
def start(request):
    return render(request,'movies/start.html')

def index(request, page_type):
    movies = Movie.objects.all()
    index_movies = Movie.objects.filter(movie_type="now_playing").order_by('-popularity')[:10]
    print(index_movies)
    if page_type == 1:
        top_rated_movies = Movie.objects.filter(movie_type="top_rated").order_by('-popularity')[:10]
        context = {
            'movies': top_rated_movies,
        }
    elif page_type == 2:
        popul_movies = Movie.objects.filter(movie_type="popular").order_by('-popularity')[:10]
        context = {
            'movies': popul_movies,
        }
    else:
        context = {
            'movies': index_movies
        }
    return render(request,'movies/index.html',context)

def detail(request,movie_pk):
    movie = get_object_or_404(Movie,pk=movie_pk)
    reviewform = ReviewForm()
    avg_score = 0
    reviews = Review.objects.filter(movie_id=movie_pk)

    url = f'https://api.themoviedb.org/3/movie/{movie_pk}/recommendations?api_key=1dfd52c8a24a0f38f40efe41c86be13b&language=ko-KR&page=1'
    response = requests.get(url).json()
    pprint.pprint(response["results"])
    new_movies = response["results"]
    for review in reviews:
        avg_score += review.score
    if reviews.count() > 0:
        avg_score /= reviews.count()
        avg_score = round(avg_score, 1)
    else:
        avg_score = 0
    peoples = []
    casts = movie.cast.all()
    for cast in casts:
        people = People.objects.filter(id=cast.id).first()
        if people:
            peoples.append(people)
    context = {
        'movie' : movie,
        'new_movies': new_movies,
        'form' : reviewform,
        'avg_score': avg_score,
        'peoples': peoples
    }
    return render(request,'movies/detail.html', context)

@login_required
def review(request, movie_pk):
    reviews = Review.objects.filter(movie_id=movie_pk)
    movie = get_object_or_404(Movie,pk=movie_pk)
    reviewForm = ReviewForm(request.POST)
    if reviewForm.is_valid():
        review = reviewForm.save(commit=False)
        review.movie_id = movie_pk
        review.user = request.user
        review.save()
        return redirect('movies:detail', movie_pk)
    context = {
        'movie' : movie,   
        'form' : reviewForm
    }
    return render(request,'movies/detail.html', context)
    
@require_POST
def review_delete(request, movie_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user == review.user:
        review.delete()
        messages.success(request, '댓글이 삭제되었습니다.')
        return redirect('movies:detail', movie_pk)
    else:
        return HttpResponseForbidden

def review_update(request, movie_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    review.content = request.POST.get('content') or review.content or ''
    review.score = request.POST.get('score') or review.score
    review.save()
    return redirect('movies:detail',movie_pk)


@login_required
def like(request, movie_pk):
    if request.is_ajax():
        movie = get_object_or_404(Movie, pk=movie_pk)
        is_liked = True
        if request.user in movie.like_users.all():
            movie.like_users.remove(request.user)
            is_liked = False
        else:
            movie.like_users.add(request.user)
            is_liked = True
        context = {
            'is_liked' : is_liked,
            'like_count' : movie.like_users.count()
        }
        return JsonResponse(context)
    else:
        return HttpResponseForbidden


def recommand(request):
    movie = Movie.objects.all()
    context = {
        'movies' : movies
    }
    return render(request,'movies/recommand.html',context)
    
def search(request):
    query = request.GET.get('search_title')
    if query:
        title_movies = Movie.objects.filter(title__icontains=query)
        description_movies = Movie.objects.filter(description__icontains=query)
        des_movies = description_movies.difference(title_movies)
        context = {
            "search_title": query,
            "title_movies" : title_movies,
            "des_movies" : des_movies
        }
        return render(request,'movies/search.html',context)
    else:
        return redirect('movies:index', 0)
