from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail_article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('update_article/<slug:slug>/', views.update, name='update'),
    path('create_article/', views.create_article, name='create_article'),
    path('delete_article/<slug:slug>/', views.delete_article, name='delete_article'),
    path('articles/<str:username>/', views.user_articles, name='user_articles'),
]
