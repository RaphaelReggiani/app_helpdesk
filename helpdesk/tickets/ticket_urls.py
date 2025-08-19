from django.urls import path
from . import ticket_views

urlpatterns = [

    path('', ticket_views.ticket_list, name='ticket_list'),
    path('create/', ticket_views.ticket_create, name='ticket_create'),
    path('<int:pk>/', ticket_views.ticket_detail, name='ticket_detail'),
    path('tickets_staff/', ticket_views.tickets_staff, name='tickets_staff'),
]
