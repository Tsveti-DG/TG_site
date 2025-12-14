from django.contrib import admin
from .models import Newspaper


@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    list_display = ("issue_number", "title", "published_at")
    list_filter = ("published_at",)
    ordering = ("-published_at", "-issue_number")
    search_fields = ("title",)

    fields = ("issue_number", "title", "published_at", "pdf", "cover_image")
