from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from helpdesk.tickets.ticket_models import Ticket, TicketMessage
from .serializers import UserSerializer, TicketSerializer, TicketMessageSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Ticket.objects.all()
        if user.role != 'suporte':
            queryset = queryset.filter(created_by=user)

        status_filter = self.request.query_params.get('status')
        priority_filter = self.request.query_params.get('priority')
        category_filter = self.request.query_params.get('category')

        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)
        if category_filter:
            queryset = queryset.filter(category=category_filter)

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['patch'], url_path='status')
    def change_status(self, request, pk=None):
        ticket = self.get_object()
        if request.user.role != 'suporte':
            return Response({'detail': 'Permissão negada'}, status=status.HTTP_403_FORBIDDEN)

        status_value = request.data.get('status')
        priority_value = request.data.get('priority')
        assigned_id = request.data.get('assigned_to')

        if status_value:
            ticket.status = status_value
        if priority_value:
            ticket.priority = priority_value
        if assigned_id:
            ticket.assigned_to = User.objects.filter(id=assigned_id, role='suporte').first()
        else:
            ticket.assigned_to = None

        ticket.save()
        serializer = self.get_serializer(ticket)
        return Response(serializer.data)

