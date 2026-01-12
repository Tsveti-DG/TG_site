from django.contrib import admin
from gallery.models import GalleryImage
from .models import CreativeWork


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    fk_name = "creative_work"
    extra = 1
    fields = ("image", "caption", "order")
    ordering = ("order",)
    verbose_name = "Снимка"
    verbose_name_plural = "Снимки"


@admin.register(CreativeWork)
class CreativeWorkAdmin(admin.ModelAdmin):
    fields = (
        "title",
        "author",
        "published_at",
        "content",
        "image",
        "code",
    )
    readonly_fields = ("code",)
    list_display = ("title", "author", "published_at")
    search_fields = ("title", "author", "content")
    ordering = ("-published_at",)
    inlines = [GalleryImageInline]
