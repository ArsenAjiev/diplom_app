from django.contrib import admin

# Register your models here.

from news.models import News


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'pubDate', 'link', 'image')

admin.site.register(News, NewsAdmin)