from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name = "Homepage"),
    path("blogpost/<int:id>/", views.blogpost, name = "blogHome"),
]