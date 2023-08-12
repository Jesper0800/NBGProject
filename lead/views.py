from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.views.generic import View, DetailView

from django.core.mail import EmailMessage
from tealcrm.settings import EMAIL_HOST_USER
from django.utils.decorators import method_decorator


from .forms import AddLeadForm,AddCommentForm
from .models import Lead, Comment

from client.models import Client


@login_required
def leads_list(request):
    leads = Lead.objects.filter(created_by=request.user, converted_to_client=False)

    return render(request, 'lead/leads_list.html',{
        'leads': leads
    })

class LeadDetailView(DetailView):
    model = Lead

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['form'] = AddCommentForm()

        return context

    def get_queryset(self):
        queryset = super(LeadDetailView, self).get_queryset()

        return queryset.filter(pk=self.kwargs.get('pk'))

@login_required
def leads_delete(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
    lead.delete()

    messages.success(request, 'The lead has been deleted')
    
    return redirect('leads_list')

class AddCommentView(View):
    model = Comment
    def post(self, request, *args, **kwargs):
        pk= kwargs.get('pk')

        form = AddCommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.lead_id = pk
            comment.created_by = request.user
            comment.save()

        return redirect('leads_list')

@login_required
def leads_edit(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
    
    if request.method == 'POST':
        form = AddLeadForm(request.POST, instance=lead)

        if form.is_valid():
            form.save()

            messages.success(request, 'The changes are saved')

            return redirect('leads_list')
    else:
        form = AddLeadForm(instance=lead)

    return render(request,'lead/leads_edit.html', {
        'form': form
    })

@login_required
def add_lead(request):
    if request.method == 'POST':
        form = AddLeadForm(request.POST)

        if form.is_valid():
            lead = form.save(commit=False)
            lead.created_by = request.user
            lead.save()

            messages.success(request, 'The lead has been created')

            return redirect('leads_list')
    else:
        form = AddLeadForm()

    return render(request,'lead/add_lead.html', {
        'form': form
    })

@login_required
def convert_to_client(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)

    client= Client.objects.create(
        name=lead.name,
        email=lead.email,
        description=lead.description,
        created_by=request.user,
        contact_datum_1=lead.contact_datum_1,
        contact_datum_2=lead.contact_datum_2,
        contact_datum_3=lead.contact_datum_3,
        lead_datum=lead.lead_datum,
        kvk=lead.kvk,
        pakket=lead.pakket,
        contact_persoon_email=lead.contact_persoon_email,
        contact_persoon=lead.contact_persoon,
        address_1=lead.address_1,
        woon_plaats=lead.woon_plaats,
        firma_type=lead.firma_type,
        telefoon_nummer=lead.telefoon_nummer,
        vak_gebied=lead.vak_gebied,
    )
    
    lead.converted_to_client = True
    subject = 'Welkom bij de Nationale Bedrijfs Gids!'
    message = 'Geachte' + '' + lead.name + 'Welkom bij de Nationale Bedrijfs Gids!'
    recipient_list = [lead.contact_persoon_email]
    send_mail(subject, message, EMAIL_HOST_USER, recipient_list, fail_silently=True)
    lead.save()

    messages.success(request, 'The lead is promoted to a client.')

    return redirect('leads_list')