from django.urls import path
from . import views, models


app_name = 'posts'
urlpatterns = [
 path('', views.index, name='index'),
 path('<int:posts_id>/create_comment', views.create_comment, name='create_comment'),
 path('', views.like, name='like'),
 path('',  views.dislike, name='dislike'),
 path('<int:posts_id>/', views.detail, name='detail'),
 path('', views.PostsList.as_view()),
 path('posts/add', views.PostsList.as_view()),
 path('posts/<int:posts_id>/edit/', views.edit_post, name='edit_post'),
 path('posts/<int:posts_id>/delete/', views.delete_post, name='delete_post'),

]
