from django.urls import path
from . import views

urlpatterns = [
    path('check/', views.check_file, name='check_file'),
    path('upload/', views.upload_file, name='upload_file'),
    path('upload/success/', views.upload_file, name='upload_file_success'),
    path('data/', views.data_dump, name='data_dump'),
    path('', views.home_page, name='home_page'),
    path('collaborator_dashboard/', views.home_page, name='index.html'),
    path('login/', views.home_page, name='index.html'),
    path('dashboard/', views.home_page, name='index.html'),
    path('report/', views.home_page, name='index.html'),
]
