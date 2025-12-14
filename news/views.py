# news/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .models import News
from gallery.models import GalleryAlbum  # за related_albums в детайла


def news_list(request):
    news = News.objects.all()
    paginator = Paginator(news, 5)  # 5 новини на страница
    page = request.GET.get('page')
    news_page = paginator.get_page(page)

    return render(request, 'news/news_list.html', {'news_page': news_page})


def news_detail(request, slug):
    article = get_object_or_404(News, slug=slug)

    # Албуми, свързани с тази новина
    related_albums = GalleryAlbum.objects.filter(related_news=article)

    return render(request, "news/news_detail.html", {
        "article": article,
        "related_albums": related_albums,
    })


def creativity(request):
    return render(request, 'news/creativity.html')
