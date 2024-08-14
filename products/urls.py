from django.urls import path
from django.urls import re_path
from . import views

urlpatterns = [
    path('', views.ProductsListView.as_view(), name='products_list_page'),
    path('category', views.ProductCategories, name='categories_page'),
    path('cat/<categorys>', views.ProductsListView.as_view(), name='products_category'),
    path('brand/<brand>', views.ProductsListView.as_view(), name='products_brand'),
    path('car/<cars>', views.ProductsListView.as_view(), name='products_cars'),
    path('brand/<brand>/cat/<categorys>', views.ProductsListView.as_view(), name='products_by_category_and_brand'),
    path('عمده', views.omdeh, name='omdeh_page'),
    re_path(r'^(?P<slug>[-\w]+)$', views.ProductsDetailView.as_view(), name='products_detail_page'),
    path('add-products-comment/', views.add_products_comment, name='add_products_comment'),
    path('product/', views.product_acces_componnetnt, name='product_acces_component'),
]
