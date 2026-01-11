# news/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.urls import reverse

from .models import News
# from gallery.models import GalleryAlbum  # за related_albums в детайла


def news(request):
    return render(request, "news/news.html")


def news_list(request):
    news = News.objects.all()
    paginator = Paginator(news, 6)  # 6 новини на страница
    page = request.GET.get('page')
    news_page = paginator.get_page(page)

    return render(request, 'news/news_list.html', {'news_page': news_page})


def news_detail(request, code):
    article = get_object_or_404(News, code=code)

    related_albums = article.related_albums.all()

    context = {
        "article": article,
        "related_albums": related_albums,
        "news_list_url": reverse("news:news_list"),
    }

    return render(request, "news/news_detail.html", context)


def creativity(request):
    return render(request, 'news/creativity.html')
