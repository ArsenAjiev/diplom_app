from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.conf import settings
from datetime import datetime
import requests
from django.core.paginator import Paginator

from omdb import OMDBClient
from movie.models import Movie, CartMovie, Cart
from movie.forms import UserRegisterForm, MovieForm
from movie.forms import AddCommentForm

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
                form = MovieForm()

        if err_msg:
            message = err_msg
            message_class = 'alert alert-danger'

        else:
            message = 'Movie added successfully'
            message_class = 'alert alert-success'

    movies = Movie.objects.order_by("-released")
    num_movies = Movie.objects.all().count()

    paginator = Paginator(movies, 5)
    page_number = request.GET.get("page")
    movies = paginator.get_page(page_number)

    return render(request, "index.html",
                  {"movies": movies, "form": form, "message": message, 'message_class': message_class, "num_movies": num_movies})


def delete_movie(request, movie_pk):
    Movie.objects.get(pk=movie_pk).delete()
    return redirect('home')


def profile(request):
    my_movie = CartMovie.objects.all().filter(cart_ref__customer_id=request.user.pk)
    paginator = Paginator(my_movie, 10)
    page_number = request.GET.get("page")
    my_movie = paginator.get_page(page_number)
    return render(request, './main/profile.html', {'my_movie': my_movie})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Вы успешно зарегистрировались")
            Cart.objects.create(customer_id=request.user.pk)
            return redirect('home')
        else:
            messages.error(request, "Ошибка регистрации")
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register_user.html', {"form": form})


def add_movie(request, movie_pk):
    #  cоздал экземпляр 'active_user' класса Cart с фктивным пользователем
    #  обратился к id экземпляра  Cart при добавлении в БД
    active_user = Cart.objects.get(customer_id=request.user.pk)
    new_pk = movie_pk
    existing_movie_pk_count = CartMovie.objects.filter(cart_ref_id=active_user.pk, movie_ref_id=new_pk).count()
    if existing_movie_pk_count == 0:
        print(movie_pk)
        print(request.user.pk)
        CartMovie.objects.create(cart_ref_id=active_user.pk, movie_ref_id=movie_pk)
        messages.success(request, "фильм успешно добавлен в ваш профиль")
        return redirect('home')
    else:
        messages.error(request, 'Фильм уже в вашем профиле.')
    return redirect('home')


def delete_user_movie(request, movie_pk):
    active_user = Cart.objects.get(customer_id=request.user.pk)
    CartMovie.objects.get(cart_ref_id=active_user.pk, movie_ref_id=movie_pk).delete()
    return redirect('profile')


# def my_comment(request):
#     Comments = CartMovie.objects.all().filter(cart_ref__customer_id=request.user.pk).order_by("-updated_at")
#     paginator = Paginator(Comments, 4)
#     page_number = request.GET.get("page")
#     Comments = paginator.get_page(page_number)
#     return render(request, './main/my_comment.html', {'Comments': Comments})


def comment(request):
    All_comment = CartMovie.objects.all().order_by("-updated_at")
    paginator = Paginator(All_comment, 10)
    page_number = request.GET.get("page")
    All_comment = paginator.get_page(page_number)
    return render(request, 'main/comment.html', {'All_comment': All_comment})


def edit_comment(request, movie_pk):
     #  cоздал экземпляр 'active_user' класса Cart с фктивным пользователем
     #  обратился к id экземпляра  Cart при добавлении в БД
    active_user = Cart.objects.get(customer_id=request.user.pk)
    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            CartMovie.objects.filter(cart_ref_id=active_user.pk, movie_ref_id=movie_pk).update(comment=form.cleaned_data["comment"])
            return redirect('comment')
            pass
    else:
        form = AddCommentForm()
    Comments = CartMovie.objects.filter(cart_ref_id=active_user.pk, movie_ref_id=movie_pk)
    return render(request, 'main/edit_comment.html', {'Comments': Comments, 'form': form})


def movie_detail(request, movie_pk):
    movie = Movie.objects.get(id=movie_pk)
    return render(request, 'main/movie_detail.html', {'movie': movie})

