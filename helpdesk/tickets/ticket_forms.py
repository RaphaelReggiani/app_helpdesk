from django import forms
from .ticket_models import Ticket, TicketMessage

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'category', 'priority', 'attachment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = "Título"
        self.fields['description'].label = "Descrição"
        self.fields['category'].label = "Categoria"
        self.fields['priority'].label = "Prioridade"
        self.fields['attachment'].label = "Anexo"

class TicketMessageForm(forms.ModelForm):
    class Meta:
        model = TicketMessage
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-gray-900 outline outline-1 outline-blue-400 focus:outline-2 focus:outline-blue-600 sm:text-sm'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].label = "Mensagem"

class TicketUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status', 'priority']
        labels = {
            'status': 'Status',
            'priority': 'Prioridade',
        }

class AssignTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['assigned_to']
        labels = {
            'assigned_to': 'Atribuir para'
        }
