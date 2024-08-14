from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article_list_view'),
    path('<category>', views.ArticleListView.as_view(), name='article_category_view'),
    path('<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail_page'),
    path('add-article-comment/', views.add_article_comment, name='add_article_comment')
]
