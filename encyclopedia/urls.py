from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("wiki", views.randomPage, name="random"),
    path("wiki/<str:item>", views.show_item, name="item"),
    path("edit", views.index, name="index"),
    path("search", views.search, name="search"),
]
