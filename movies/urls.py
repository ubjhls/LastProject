from django.contrib import admin
from django.urls import path,include
from . import views

app_name= 'movies'

urlpatterns = [
    path('',views.start, name='start'),
    path('index/<int:page_type>/', views.index, name='index'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('<int:movie_pk>/reivew', views.review, name='review'),
    path('<int:movie_pk>/reviews/<int:review_pk>/delete', views.review_delete, name='review_delete'),
    path('<int:movie_pk>/like/', views.like , name='like_movie'),
    path('recommand', views.recommand, name='recommand'),
    path('search/',views.search,name="search"),
    ]
