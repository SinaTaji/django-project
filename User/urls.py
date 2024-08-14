from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register_page'),
    path('resetpass/<active_code>', views.ResetPasswordView.as_view(), name='reset_pass_page'),
    path('active_user/<email_active_code>', views.ActiveUserView.as_view(), name='active_user_page'),
    path('login/', views.LoginUserView.as_view(), name='login_page'),
    path('forget-pass/', views.ForgotPasswordView.as_view(), name='forgot_pass_page'),
    path('logout/', views.LogOutView.as_view(), name='logout_page'),
]
