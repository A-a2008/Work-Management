from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("litigation/new/", views.litigation_new, name="litigation_new")
]