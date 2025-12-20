from django.contrib import admin
from .models import GalleryAlbum, GalleryImage


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 2
    fields = ("image", "caption", "order")
    show_change_link = True


@admin.register(GalleryAlbum)
class GalleryAlbumAdmin(admin.ModelAdmin):
    list_display = ("title", "code", "order", "created_at", "related_news")
    list_editable = ("order",)
    readonly_fields = ("code",)
    ordering = ("-created_at", "order", "title")
    inlines = [GalleryImageInline]
