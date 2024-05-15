from django.urls import path
from . import views

urlpatterns = [
    path('check/', views.check_file, name='check_file'),
    path('upload/', views.upload_file, name='upload_file'),
    path('upload/success/', views.upload_file, name='upload_file'),
]
