from django.urls import path
from . import ticket_views

urlpatterns = [

    path('tickets/', ticket_views.ticket_list, name='ticket_list'),
    path('tickets/create/', ticket_views.ticket_create, name='ticket_create'),
    path('tickets/<int:pk>/', ticket_views.ticket_detail, name='ticket_detail'),
]
