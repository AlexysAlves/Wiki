from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.page, name="page"),
    path("search", views.search, name="search"),
    path("new_page", views.create, name="new_page"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("wiki/", views.randomP, name="random")
]
