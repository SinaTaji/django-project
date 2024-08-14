from django.urls import path
from . import views

urlpatterns = [
    path('',views.HomeView.as_view(), name='home_page'),
    path('search/',views.searchbox_component, name='search_box'),
    path('search-resualt/',views.searchbox_resualt, name='search_box_resualt'),
]