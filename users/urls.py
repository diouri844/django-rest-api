# users/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('create_customer/', views.create_customer, name='create_customer'),
    path('list_customers/', views.list_customers, name='list_customers'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
]