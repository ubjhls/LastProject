from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control customTextInput',
                'placeholder': '아이디'
                }
            ),label=''
        )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control customTextInput',
                'placeholder': '닉네임'
                }
            ),label=''
        )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control customTextInput',
                'placeholder': '이메일'
                }
            ),label=''
        )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control customTextInput',
                'placeholder': '비밀번호'
                }
            ),label=''
        )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control customTextInput',
                'placeholder': '비밀번호 확인'
                }
            ),label=''
        )
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'email','password1','password2','image')
        helptext=''




class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )