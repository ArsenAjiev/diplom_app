from django.contrib import admin
from movie.models import Movie, Cart, CartMovie

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "year", "created_at", "image", "imdb_id")
    fields = ("title", "year",  "created_at", "image", "imdb_id")
    readonly_fields = ("created_at",)
    search_fields = ("title", "year")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("customer", "comment")


@admin.register(CartMovie)
class CartMovieAdmin(admin.ModelAdmin):
    list_display = ("cart_ref", "movie_ref", "comment")
    readonly_fields = ("updated_at",)