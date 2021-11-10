from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.conf import settings
from datetime import datetime
import requests

from omdb import OMDBClient
from movie.models import Movie
from movie.forms import UserRegisterForm, MovieForm


IMDB_API_KEY = '17cdc959'
client = OMDBClient(apikey=IMDB_API_KEY)
movie_all = Movie.objects.all()


def index(request):
    form = MovieForm(request.POST)
    err_msg = ''
    message = ''
    message_class = ''

    if request.method == "POST":
        form = MovieForm(request.POST)
        if form.is_valid():

            title_api = form.cleaned_data['title']
            year_api = form.cleaned_data['year']

            json_data = client.get(title=title_api, year=year_api, tomatoes=True, fullplot=True)
            if not json_data:
                return redirect('home')

            url = json_data["poster"]
            name = json_data["title"]
            response = requests.get(url, stream=True)
            file_name = f"{name}.jpeg"
            with open(settings.MEDIA_ROOT / file_name, "wb") as out_file:
                out_file.write(response.content)

            new_imdb = json_data['imdb_id']
            existing_imdb_id_count = Movie.objects.filter(imdb_id=new_imdb).count()
            if existing_imdb_id_count == 0:
                Movie.objects.create(
                    title=json_data["title"],
                    year=json_data["year"],
                    runtime=json_data["runtime"],
                    genre=json_data["genre"],
                    country=json_data["country"],
                    image=file_name,
                    imdb_id=json_data['imdb_id'],
                    imdb_rating=json_data['imdb_rating'],
                    imdb_votes=json_data['imdb_votes'],
                    released=datetime.strptime(json_data['released'], "%d %b %Y"),
                    plot=json_data['plot'],
                )
                form = MovieForm()
                pass
            else:
                err_msg = 'Movie already exist in the database!'

        if err_msg:
            message = err_msg
            message_class = 'alert alert-danger'

        else:
            message = 'Movie added successfully'
            message_class = 'alert alert-success'

    movies = Movie.objects.order_by("-released")

    return render(request, "index.html",
                  {"movies": movies, "form": form, "message": message, 'message_class': message_class})



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


