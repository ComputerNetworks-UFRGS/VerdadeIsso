from django.urls import path
from . import views
from .views import MyLoginView

urlpatterns = [
    path('check/', views.check_file, name='check_file'),
    path('upload/', views.upload_file, name='upload_file'),
    path('addSource/', views.add_source, name='add_source'),
    path('upload/success/', views.upload_file, name='upload_file_success'),
    path('data/', views.data_dump, name='data_dump'),
    path('data/<int:value_id>/', views.fake_samples, name='data_dump'),
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', MyLoginView.as_view(template_name='App/templates/login/login.html'),name='login'),
]
