from django.contrib import admin

from gallery.models import GalleryImage, GalleryVideo
from .models import News


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    fk_name = "news"
    extra = 1
    fields = ("image", "caption", "order")
    ordering = ("order",)
    verbose_name = "Снимка"
    verbose_name_plural = "Снимки"
    show_change_link = True


class GalleryVideoInline(admin.TabularInline):
    model = GalleryVideo
    fk_name = "news"
    extra = 1
    fields = ("video_url", "title", "order")
    ordering = ("order",)
    verbose_name = "Видео"
    verbose_name_plural = "Видеа"
    show_change_link = True


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    fields = ("title", "code", "content", "created_at", "image")
    list_display = ("title", "created_at", "code")
    search_fields = ("title", "content")
    ordering = ("-created_at",)
    readonly_fields = ("code", "created_at")
    inlines = [GalleryImageInline, GalleryVideoInline]
