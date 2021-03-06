from django.db import models
from django.conf import settings
from django.urls import reverse


#  модель для добавления фильмов в базу данных
class Movie(models.Model):
    title = models.CharField(max_length=255, verbose_name='название')
    year = models.IntegerField(verbose_name='год производства')
    runtime = models.CharField(max_length=255, verbose_name='длительность')
    genre = models.CharField(max_length=255, verbose_name='жанр фильма')
    country = models.CharField(max_length=255, verbose_name='страна')
    image = models.ImageField(null=True, blank=True, verbose_name='постер')
    imdb_id = models.CharField(max_length=255, verbose_name='imdb id')
    released = models.CharField(max_length=255, verbose_name='премьера в мире')
    plot = models.TextField(verbose_name='сюжет')
    imdb_rating = models.CharField(max_length=255, verbose_name='рейтинг')
    imdb_votes = models.CharField(max_length=255, verbose_name='количество голосов')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='опубликовано')

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        # Возвращает url-адрес для доступа к определенному экземпляру книги.
        return reverse('movie_detail', kwargs={'movie_pk': self.pk})


#  модель которая создает профиль для пользователя.
#  один пользователь может иметь только один профиль (OneToOneField)
class Cart(models.Model):
    customer = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='prof', verbose_name='пользователь')
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name='примечание')

    def __str__(self):
        return self.customer.username


#  модель которая позволяет добавить фильм в профиль пользователю
class CartMovie(models.Model):
    cart_ref = models.ForeignKey(Cart, related_name='cart', on_delete=models.CASCADE, verbose_name='ссылка на Cart')
    movie_ref = models.ForeignKey(Movie, related_name='movie', on_delete=models.CASCADE, verbose_name='ссылка на Movie')
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name='отзыв')
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name=" отзыв добавлен")