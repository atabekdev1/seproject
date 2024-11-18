from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.profile_settings, name='profile_settings'),
    path('signup/', views.signup, name='signup'),
    
]