from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [

    path('', views.home_page, name="home_page"),
    path('posts/', views.posts_list, name='posts_list'),
    path('posts/<slug:post>/', views.post_detail, name='post_detail')

]