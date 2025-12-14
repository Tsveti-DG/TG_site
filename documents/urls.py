# documents/urls.py
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
        "<slug:supercategory_slug>/",
        views.documents_by_supercategory,
        name="documents_by_super",
    ),
]
