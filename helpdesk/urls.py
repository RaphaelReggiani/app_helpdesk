from django.urls import path
from .views import auth_view, logout_view, profile_view

urlpatterns = [
    path('login/', auth_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
]
