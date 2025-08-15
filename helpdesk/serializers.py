from rest_framework import serializers
from django.contrib.auth import get_user_model
from helpdesk.tickets.ticket_models import Ticket, TicketMessage

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'phone', 'country', 'profile_photo', 'password', 'is_staff', 'is_superuser']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class TicketMessageSerializer(serializers.ModelSerializer):
    sent_by_email = serializers.SerializerMethodField()

    class Meta:
        model = TicketMessage
        fields = ['id', 'ticket', 'message', 'sent_by', 'sent_by_email', 'created_at']

    def get_sent_by_email(self, obj):
        return obj.sent_by.email if obj.sent_by else None

class TicketSerializer(serializers.ModelSerializer):
    created_by_email = serializers.SerializerMethodField()
    assigned_to_email = serializers.SerializerMethodField()
    messages = TicketMessageSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id', 'title', 'description', 'category', 'priority', 'status',
            'protocol_number', 'attachment', 'created_by', 'created_by_email',
            'assigned_to', 'assigned_to_email', 'created_at', 'updated_at', 'messages'
        ]

    def get_created_by_email(self, obj):
        return obj.created_by.email if obj.created_by else None

    def get_assigned_to_email(self, obj):
        return obj.assigned_to.email if obj.assigned_to else None
