"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from site_setting.views import custom_404_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('home.urls')),
    path('order/',include('order_list.urls')),
    path('article/',include('article.urls')),
    path('',include('contactus_aboutus.urls')),
    path('product/',include('products.urls')),
    path('user/',include('User.urls')),
    path('user-panel/',include('user_panel.urls')),
    path('',include('site_setting.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = custom_404_view