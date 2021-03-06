from django.shortcuts import render
from news.models import News
import urllib.request, json
from django.core.paginator import Paginator


news_all = News.objects.all()


#  отображает отсортированный список новостей
def news_view(request):
    #  получение и обработка новостей
    with urllib.request.urlopen(
            "https://api.rss2json.com/v1/api.json?rss_url=http%3A%2F%2Ffeeds.feedburner.com%2Fmovieweb_news") as url:
        data = json.loads(url.read().decode())

    lenn = len(data['items'])
    for i in range(lenn):
        new_title = data['items'][i]['title']
        existing_title_count = News.objects.filter(title=new_title).count()
        if existing_title_count == 0:
            News.objects.create(
                title=data['items'][i]['title'],
                pubDate=data['items'][i]['pubDate'],
                link=data['items'][i]['link'],
                image=data['items'][i]['enclosure']['link'])
    news = News.objects.order_by("-pubDate")

    paginator = Paginator(news, 10)
    page_number = request.GET.get("page")
    news = paginator.get_page(page_number)

    return render(request, "news/news.html", {"news": news})


