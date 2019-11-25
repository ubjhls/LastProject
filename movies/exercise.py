from django.shortcuts import render,redirect,get_object_or_404
from .models import Movie, Genre, Review

a = Review.objects.all().aggregate(Avg('score'))
print(a)


