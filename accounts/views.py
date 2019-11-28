from django.shortcuts import render
from django.shortcuts import render,redirect, get_object_or_404
from .models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .forms import CustomUserCreationForm, LoginForm
from django.contrib.auth import login as django_login, logout as django_logout, authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request,'accounts/index.html',context)

def signup(request):
    if request.user.is_authenticated:
        return redirect('movies:index',0)
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('movies:index',0)
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/signup.html', context)
        

def detail(request, user_pk):
    User = get_user_model()
    user = User.objects.get(pk=user_pk)
    context = {
        'user_profile' : user,
    }
    return render(request,'accounts/detail.html', context)

def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(
                username=username,
                password=password
            )

            if user:
                django_login(request, user)
                return redirect('movies:index', 0)
            login_form.add_error(None, '아이디 또는 비밀번호가 올바르지 않습니다')
    else:
        login_form = LoginForm()
    context = {
        'login_form': login_form,
    }
    return render(request, 'accounts/login.html', context)



def logout(request):
    auth_logout(request)
    return redirect('movies:index', 0)

@login_required
def follow(request, account_pk):
    User = get_user_model()
    obama = get_object_or_404(User, pk=account_pk)
    if request.user != obama:
        if request.user in obama.followers.all():
            obama.followers.remove(request.user)
        else:
            obama.followers.add(request.user)
    return redirect('accounts:detail', account_pk)