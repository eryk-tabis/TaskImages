from django.urls import path
from . import views

urlpatterns = [
    path('', views.ImageListCreateAPI.as_view(), name='image_list_create'),
]
