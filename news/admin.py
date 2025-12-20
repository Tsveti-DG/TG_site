from django.contrib import admin
from .models import News, NewsImage


class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 1
    fields = ("image", "caption")
    show_change_link = True


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    fields = ("title", "code", "content", "image", "youtube_id")
    list_display = ("title", "created_at", "code")
    search_fields = ("title", "content")
    readonly_fields = ("code",)
    ordering = ("-created_at",)
    inlines = [NewsImageInline]
