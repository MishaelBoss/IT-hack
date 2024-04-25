from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page),
    path('profile/', views.profile),
    path('profile_edit/', views.profile_edit),
]