from django.contrib import admin
from .models import GalleryAlbum, GalleryImage, GalleryVideo


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    fk_name = "album"
    extra = 1
    fields = ("image", "caption", "order")
    show_change_link = True


class GalleryVideoInline(admin.TabularInline):
    model = GalleryVideo
    fk_name = "album"
    extra = 1
    fields = ("video_url", "title", "order")
    show_change_link = True


@admin.register(GalleryAlbum)
class GalleryAlbumAdmin(admin.ModelAdmin):
    list_display = ("title", "code", "order", "created_at", "related_news")
    list_editable = ("order",)
    readonly_fields = ("code",)
    ordering = ("-created_at", "order", "title")
    inlines = [GalleryImageInline, GalleryVideoInline]
