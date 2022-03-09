from django.urls import path
from . import views
from .views import PostsList  # импортируем наше представление

app_name = 'posts'
urlpatterns = [
 path('', views.index, name='index'),
 path('<int:article_id>/', views.detail, name='detail'),
 path('<int:article_id>/leave_comment', views.leave_comment, name='leave_comment'),
 path('', PostsList.as_view()),

]
