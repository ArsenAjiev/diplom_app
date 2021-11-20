from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from movie.models import Movie
from datetime import date


#  форма регистрации нового пользователя
class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label="Имя пользователя", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


#  форма для добавления фильма в базу данных
class MovieForm(ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'year']


#  форма для добавления коментария
class AddCommentForm(forms.Form):
    comment = forms.CharField(max_length=255, label='Коментарий', widget=forms.Textarea(attrs={
        "class": "form-control",
        "rows": 5
    }))


#  форма для поиска фильмов по дате выхода в прокат
class AddDataForm(forms.Form):
    date_1 = forms.DateTimeField(label="Первая дата периода",
                                    initial=format(date),
                                    widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    date_2 = forms.DateTimeField(label="Вторая дата периода",
                                 initial=format(date),
                                 widget=forms.widgets.DateInput(attrs={'type': 'date'}))

