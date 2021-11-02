from django.shortcuts import render

from django.shortcuts import render, redirect
from movie.forms import UserRegisterForm
from django.contrib.auth import login, logout
from django.contrib import messages

# Create your views here.


def index(request):
    return render(request, 'index.html')


def profile(request):
    return render(request, './main/profile.html')



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Вы успешно зарегистрировались")
            return redirect('home')
        else:
            messages.error(request, "Ошибка регистрации")
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register_user.html', {"form": form})