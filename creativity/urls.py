from django.urls import path
from . import views

app_name = "creativity"

urlpatterns = [
    path(
        "",
        views.creativity_list,
        name="creativity_list",
    ),
    path(
        "<slug:code>/",
        views.creativity_detail,
        name="detail",
    ),
]
