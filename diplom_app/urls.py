"""diplom_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from movie.views import index, register, profile, add_movie, delete_movie, delete_user_movie
from movie.views import  comment, edit_comment, movie_detail, choise_genre, buy_dvd, buy_online_watch, buy_ticket
from movie.views import choise_date
from news.views import news_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('accounts/register/', register, name='register'),
    path('accounts/profile/', profile, name='profile'),
    path('news/', news_view, name='news'),
    path('add/<movie_pk>/', add_movie, name='add_movie'),
    path('delete_user_movie/<movie_pk>/', delete_user_movie, name='delete_user_movie'),
    path('delete_movie/<movie_pk>/', delete_movie, name='delete_movie'),
    path('comment/', comment, name='comment'),
    #  path('my_comment/', my_comment, name='my_comment'),
    path('edit_comment/<movie_pk>/', edit_comment, name='edit_comment'),
    path('movie_detail/<movie_pk>/', movie_detail, name='movie_detail'),
    path('movie_choise/<name>/', choise_genre, name='choise_genre'),
    path('buy_dvd/<movie_pk>/', buy_dvd, name='buy_dvd'),
    path('buy_online_watch/<movie_pk>/', buy_online_watch, name='buy_online_watch'),
    path('buy_ticket/<movie_pk>/', buy_ticket, name='buy_ticket'),
    path('choise_date/', choise_date, name='choise_date')


]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),

]