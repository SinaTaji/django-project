from django.urls import path
from . import views

urlpatterns = [
    path('about-us', views.about_us_view.as_view(), name='about_us_page'),
    path('contact-us', views.ContactUsView.as_view(), name='contact_us_page'),
    path('questions-answer', views.q_and_answer_view, name='q_and_answer_view'),
]
