from django.contrib import admin
from .models import News, NewsImage


class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 2
    fields = ("image", "caption")
    show_change_link = True


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "slug")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-created_at",)
    inlines = [NewsImageInline]
    fields = ("title", "slug", "content", "image", "youtube_id")
