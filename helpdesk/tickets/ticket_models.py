from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid

class Ticket(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Baixa'),
        ('medium', 'Média'),
        ('high', 'Alta'),
    ]
    STATUS_CHOICES = [
        ('open', 'Aberto'),
        ('in_progress', 'Em Andamento'),
        ('closed', 'Fechado'),
    ]
    CATEGORY_CHOICES = [
        ('software', 'Software'),
        ('hardware', 'Hardware'),
        ('network', 'Rede'),
        ('other', 'Outro'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    protocol_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    attachment = models.FileField(upload_to='ticket_attachments/', blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets_created')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='tickets_assigned')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.protocol_number}] {self.title}"
    
    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"

class TicketMessage(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='messages')
    message = models.TextField()
    sent_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sent_by.email} em {self.created_at}: {self.message[:20]}..."

