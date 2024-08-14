from django.urls import path
from . import views

urlpatterns = [
    path('user-basket',views.user_basket, name='user_basket_page'),
    path('user-panel',views.user_dashboard, name='user_dashboard_page'),
    path('user-panel-change-informations',views.user_change_informations.as_view(), name='user_change_informations'),
    path('user-panel-change-password',views.change_user_password.as_view(), name='user_change_password'),
    path('remove-order-detail',views.user_basket_content, name='remove_order_detail'),
    path('change-order-detail',views.change_basket_content_count, name='change_order_detail'),
    path('way-to-pay',views.way2pay, name='way2pay'),
    path('final-payment',views.finalPaymentForm_View.as_view(), name='final_payment'),
    path('faktor-component',views.faktor_component, name='faktor_component'),
    path('pay-card-to-card',views.pay_card_to_card, name='card_to_card_page'),
]