from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class Genre(models.Model):
    name = models.TextField()

class People(models.Model):
    name = models.TextField()
    profile_path = models.TextField()

class Movie(models.Model):
    title = models.TextField()
    movie_type = models.TextField()
    poster_url = models.TextField()
    description =  models.TextField()
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    video_link = models.TextField()
    popularity = models.FloatField()
    vote_average = models.FloatField()
    back_image = models.TextField()
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='like_movies',
        blank=True
        )
    cast = models.ManyToManyField(
        People,
        related_name='known_for',
        blank=True
    )
    

class Review(models.Model):
    content = models.TextField(verbose_name='한줄평')
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], verbose_name='평점')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
