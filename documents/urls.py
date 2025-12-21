from django.urls import path
from . import views

app_name = "documents"

urlpatterns = [
    path(
        "",
        views.documents_overview,
        name="documents_overview",
    ),
    path(
        "archive/",
        views.documents_archive,
        name="documents_archive",
    ),
    path(
        "<str:category_code>/",
        views.documents_by_category,
        name="documents_by_category",
    ),
]
