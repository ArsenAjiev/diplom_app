from django.contrib import admin
from movie.models import Movie

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "year", "created_at", "image", "imdb_id")
    fields = ("title", "year",  "created_at", "image", "imdb_id")
    readonly_fields = ("created_at",)
    search_fields = ("title", "year")