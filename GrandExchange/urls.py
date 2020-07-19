from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("item/<str:name>", views.item, name="item"),
]
