from django.contrib import admin
from .models import GalleryAlbum, GalleryImage


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 2
    fields = ("image", "caption", "order")
    show_change_link = True


@admin.register(GalleryAlbum)
class GalleryAlbumAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "related_news")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("order", "title")
    inlines = [GalleryImageInline]
