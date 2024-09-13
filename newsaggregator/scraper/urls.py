from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='article-list'),  # Default view for /api/articles/
    path('list/', views.article_list, name='article-list'),  # Subpath for /api/articles/list/
    path('categorize/', views.categorize_news, name='categorize-news'),  # Subpath for /categorize-news/
]
# scraper/urls.py
from django.urls import path
from .views import article_list, article_detail, article_search

urlpatterns = [
    path('', article_list, name='article-list'),
    path('<int:id>/', article_detail, name='article-detail'),
    path('search/', article_search, name='article-search'),
]
