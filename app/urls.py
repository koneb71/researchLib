
from django.urls import path, include
from app import views
from app.api.routes import router

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include(router.urls)),
    path('post', views.post_research, name='post_research'),
    path('view/<int:id>/', views.view_research, name='view_research'),
    path('pdf/<int:id>/', views.send_pdf, name='send_pdf'),
]