from django.urls import path
from . import views

urlpatterns = [
    path('', views.custom_404_view, name="404"),
]
