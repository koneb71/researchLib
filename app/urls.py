
from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post', views.post_research, name='post_research'),
    path('view/<int:id>/', views.view_research, name='view_research'),
]