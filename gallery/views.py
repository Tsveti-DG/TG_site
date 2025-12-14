# gallery/views.py
from django.shortcuts import render, get_object_or_404

from .models import GalleryAlbum


def gallery_list(request):
    albums = GalleryAlbum.objects.all()
    return render(request, 'gallery/gallery_list.html', {'albums': albums})


def gallery_detail(request, slug):
    album = get_object_or_404(GalleryAlbum, slug=slug)
    images = album.images.all()
    related_news = album.related_news

    return render(request, 'gallery/gallery_detail.html', {
        'album': album,
        'images': images,
        'related_news': related_news,
    })
