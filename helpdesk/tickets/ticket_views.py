from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .ticket_models import Ticket, TicketMessage
from .ticket_forms import TicketForm, TicketMessageForm

User = get_user_model()

@login_required(login_url='home')
def ticket_list(request):
    if request.user.role == 'suporte':
        tickets = Ticket.objects.all()
    else:
        tickets = Ticket.objects.filter(created_by=request.user)

    status_filter = request.GET.get('status')
    priority_filter = request.GET.get('priority')
    if status_filter:
        tickets = tickets.filter(status=status_filter)
    if priority_filter:
        tickets = tickets.filter(priority=priority_filter)

    return render(request, 'ticket_list.html', {'tickets': tickets})


@login_required(login_url='home')
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)

    if request.user.role != 'suporte' and ticket.created_by != request.user:
        messages.error(request, "Você não tem permissão para ver este ticket.")
        return redirect('ticket_list')

    msg_form = TicketMessageForm()

    if request.method == 'POST':
        if request.user.role == 'suporte' and ('update_ticket' in request.POST or 'assign_ticket' in request.POST):
            if 'update_ticket' in request.POST:
                ticket.status = request.POST.get('status', ticket.status)
                ticket.priority = request.POST.get('priority', ticket.priority)

            if 'assign_ticket' in request.POST:
                assigned_id = request.POST.get('assigned_to')
                if assigned_id:
                    ticket.assigned_to = User.objects.filter(id=assigned_id, role='suporte').first()
                else:
                    ticket.assigned_to = None

            ticket.save()
            messages.success(request, "Ticket atualizado com sucesso!")
            return redirect('ticket_detail', pk=ticket.pk)

        if 'send_message' in request.POST:
            msg_form = TicketMessageForm(request.POST)
            if msg_form.is_valid():
                msg = msg_form.save(commit=False)
                msg.ticket = ticket
                msg.sent_by = request.user
                msg.save()
                messages.success(request, "Mensagem enviada com sucesso!")
                return redirect('ticket_detail', pk=ticket.pk)
            else:
                messages.error(request, "Erro ao enviar mensagem. Verifique o formulário.")

    staff_users = User.objects.filter(role='suporte')
    messages_list = ticket.messages.all().order_by('created_at')

    return render(
        request,
        'ticket_detail.html',
        {
            'ticket': ticket,
            'msg_form': msg_form,
            'staff_users': staff_users,
            'messages_list': messages_list,
        }
    )

@login_required(login_url='home')
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
            messages.error(request, "Erro ao criar ticket. Verifique os campos.")
    else:
        form = TicketForm()

    return render(request, 'ticket_form.html', {'form': form})

@login_required(login_url='home')
def tickets_staff(request):
    if request.user.role == 'suporte':
        tickets = Ticket.objects.all()
    else:
        return redirect('home')

    status_filter = request.GET.get('status')
    priority_filter = request.GET.get('priority')
    if status_filter:
        tickets = tickets.filter(status=status_filter)
    if priority_filter:
        tickets = tickets.filter(priority=priority_filter)

    return render(request, 'tickets_staff.html', {'tickets': tickets})






