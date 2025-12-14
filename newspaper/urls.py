from django.urls import path
from . import views

app_name = "newspaper"

urlpatterns = [
    path("", views.newspaper_list, name="newspaper_list"),
]
