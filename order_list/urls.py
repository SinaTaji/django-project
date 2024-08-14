from django.urls import path
from . import views

urlpatterns = [
    path('add-order', views.add_order_list, name='add_order'),
    path('request/', views.send_request, name='request'),
    path('verify/', views.verify , name='verify'),
]
