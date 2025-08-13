from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .ticket_models import Ticket, TicketMessage
from .ticket_forms import TicketForm, TicketMessageForm

@login_required
def ticket_list(request):
    tickets = Ticket.objects.all()
    if not request.user.is_staff:
        tickets = tickets.filter(created_by=request.user)
    status_filter = request.GET.get('status')
    priority_filter = request.GET.get('priority')
    if status_filter:
        tickets = tickets.filter(status=status_filter)
    if priority_filter:
        tickets = tickets.filter(priority=priority_filter)
    return render(request, 'ticket_list.html', {'tickets': tickets})

@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if not request.user.is_staff and ticket.created_by != request.user:
        messages.error(request, "Você não tem permissão para ver este ticket.")
        return redirect('ticket_list')
    
    if request.method == 'POST':
        msg_form = TicketMessageForm(request.POST)
        if msg_form.is_valid():
            msg = msg_form.save(commit=False)
            msg.ticket = ticket
            msg.sent_by = request.user
            msg.save()
            messages.success(request, "Mensagem enviada com sucesso.")
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        msg_form = TicketMessageForm()

    return render(request, 'ticket_detail.html', {'ticket': ticket, 'msg_form': msg_form})

@login_required
def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            messages.success(request, "Ticket criado com sucesso!")
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        form = TicketForm()
    return render(request, 'ticket_form.html', {'form': form})
