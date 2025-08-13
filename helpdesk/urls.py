from django.urls import path, include
from . import views, password_views

urlpatterns = [

    path('tickets/', include('helpdesk.tickets.urls')),

    # HOME

    path('', views.home, name="home"),

    # URLs - Usuário

    path('login/', views.auth_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),

    # Reset de senha

    path('forgot-password/', password_views.CustomPasswordResetView.as_view(), name='forgot-password'),
    path('forgot-password/done/', password_views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', password_views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-complete/', password_views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
