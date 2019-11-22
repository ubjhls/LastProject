### Django (Pair Programming)

1. accounts App

회원가입 

```python
def signup(request):
    if request.user.is_authenticated:
        return redirect('movies:index')
    if request.method == 'POST': 
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request,user)
            return redirect('movies:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/signup.html', context)

```

로그인, 로그아웃 -  만약 로그인되어있으면 로그아웃 만 나타나고 아니라면 회원가입 로그인이 나타나도록 한다.

```python
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request,user)
            return redirect('movies:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request,'accounts/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('movies:index')
```

유저목록 - 해당유저가 작성한 평점정보, 좋아하는 영화정보, 팔로우, 팔로잉 수 출력

- views.py

```python
def detail(request, user_pk):
    User = get_user_model()
    user = User.objects.get(pk=user_pk)
    context = {
        'user_profile' : user,
    }
    return render(request,'accounts/detail.html', context)
```

- detail.html

```html
{% extends 'base.html' %}
{% block body %}

{% with user_profile.followers.all as followers %}
  <a href="{% url 'accounts:follow' user_profile.pk %}">
      {% if user in followers %} 
      팔로우취소
      {% else %}
      팔로우
      {% endif %}
  </a>
  <h2> 팔로우 : {{ user_profile.followings.all.count }} </h2>
  <h2> 팔로워 : {{ followers|length }}</h2>
{% endwith %}

<p>내가 작성한 평점 정보 </p>
{% for review in user_profile.review_set.all %}
  <p>영화 : {{review.movie.title}} <br> 내용 : {{review.content}} <br> 평점 : {{ review.score }}</p>

{% endfor %}
<hr>
<p>내가 좋아하는 영화 </p>
{% for like in user_profile.like_movies.all %}
   {{like.title}}<br>

{% endfor %}
{% endblock %} 

```

movies App

영화목록 - 모든영화목록을 index에 표시

```python
def index(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies
    }
    return render(request,'movies/index.html',context)
```

상세보기, 평점생성, 평점삭제 - json 로드해서 제목,장르등 상세정보를 표시하고 하단에 로그인한 사람만 평점을 남기고 삭제할수 있다.

- detail.html

```html
{% extends 'base.html' %}
{% block body %}
    <div>
        제목 : {{movie.title}}<hr>
        관객수 : {{movie.audience}}<hr>
        url : {{movie.poster_url}}<hr>
        요약 : {{movie.description}}<hr>
        장르 : {{movie.genre.name}}<hr>
    </div>

{% if user.is_authenticated %}
<form action="{% url 'movies:like_movie' movie.pk %}" method="POST">
  {% csrf_token %}
  {% if user in movie.like_users.all %}
  <input type="submit" value="좋아요 취소">
  {% else %}
  <input type="submit" value="좋아요">
  {% endif %}
</form>
{% endif %}

<p>
{{ movie.like_users.all.count }} 명이 좋아합니다.
</p>

{% for review in movie.review_set.all %}
    <p>
        <hr>작성자: {{review.user}} <br> 점수 : {{review.score}}<br> 내용 :{{review.content}}<br>
    </p>
    <form action='reviews/{{review.pk}}/delete' method='POST'>
        {% csrf_token %}
        <input type='submit' value='삭제'>
        </form>
{% endfor %}

<form action="{% url 'movies:review' movie.pk %}" method='POST'>
    {% csrf_token %}
    {{form.as_p}}
    <input type='submit' value='등록'>
</form>
{% endblock %}

```

- views.py

```python
def detail(request,movie_pk):
    movie = get_object_or_404(Movie,pk=movie_pk)
    reviewform = ReviewForm()
    context = {
        'movie' : movie,   
        'form' : reviewform
    }
    return render(request,'movies/detail.html', context)

@login_required
def review(request, movie_pk):
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

def reviewDelete(request, movie_pk,review_pk):
    review = get_object_or_404(Review,pk=review_pk)
    if request.user == review.user:
        review.delete()
    
    return redirect('movies:detail', movie_pk)
```

좋아요 - 로그인한 유저만 좋아요 기능이 가능하고 좋아하는 영화를 담을 수 있도록 구현

- views.py

```python
@login_required
def like(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    if request.user in movie.like_users.all():
        movie.like_users.remove(request.user)
    else:
        movie.like_users.add(request.user)
    return redirect('movies:detail', movie_pk)
```

- html

```html
{% if user.is_authenticated %}
<form action="{% url 'movies:like_movie' movie.pk %}" method="POST">
  {% csrf_token %}
  {% if user in movie.like_users.all %}
  <input type="submit" value="좋아요 취소">
  {% else %}
  <input type="submit" value="좋아요">
  {% endif %}
</form>
{% endif %}

<p>
{{ movie.like_users.all.count }} 명이 좋아합니다.
</p>
```

- git 으로 처음 협업을 해본결과 익숙하지 않아 불편함을 느꼈지만 익숙해지만 편해질것 같았다.

![캡처](.\캡처.JPG)