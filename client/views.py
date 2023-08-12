import csv
from typing import Any
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models.query import QuerySet
from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import ListView,DetailView,DeleteView,View

from django.utils.decorators import method_decorator

from .forms import AddClientForm,AddFileForm,AddCommentForm2
from .models import Client, ClientFile, Comment
from .filters import ClientFilter

@login_required
def clients_export(request):
    clients = Client.objects.filter()

    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="klanten.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(['Client', 'Pakket', 'Contact Persoon', 'Contact Persoon Email'])

    for client in clients:
        writer.writerow([client.name, client.pakket, client.contact_persoon, client.contact_persoon_email])

    return response

class ClientListView(ListView):
    model = Client
    myFilter = ClientFilter()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = super(ClientListView, self).get_queryset()
        return queryset.filter()
    
class ClientDetailView(DetailView):
    model = Client

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['form'] = AddCommentForm2()
        context['fileform'] = AddFileForm()

        return context

    def get_queryset(self):
        queryset = super(ClientDetailView, self).get_queryset()

        return queryset.filter(pk=self.kwargs.get('pk'))
    
class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('clients_list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_queryset(self):
        queryset = super(ClientDeleteView, self).get_queryset()

        return queryset.filter(pk=self.kwargs.get('pk'))
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    
class AddFileView(View):
    def post(self, request, *args, **kwargs):
        pk= kwargs.get('pk')

        form = AddFileForm(request.POST, request.FILES)

        if form.is_valid():
            file = form.save(commit=False)
            file.client_id = pk
            file.created_by = request.user
            file.save()

        return redirect('clients_list')


@login_required
def clients_add(request):
    if request.method == 'POST':
        form = AddClientForm(request.POST)

        if form.is_valid():
            lead = form.save(commit=False)
            lead.created_by = request.user
            lead.save()

            messages.success(request, 'Het klant account is aangemaakt')

            return redirect('client_list')
    else:
        form = AddClientForm()

    return render(request,'client/clients_add.html', {
        'form': form
    })

class AddCommentView2(View):
    model = Comment
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        form = AddCommentForm2(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.client_id = pk
            comment.created_by = request.user
            comment.save()

        return redirect('clients_list')

@login_required
def clients_edit(request, pk):
    client = get_object_or_404(Client, pk=pk)
    
    if request.method == 'POST':
        form = AddClientForm(request.POST, instance=client)

        if form.is_valid():
            form.save()

            messages.success(request, 'The changes are saved')

            return redirect('clients_list')
    else:
        form = AddClientForm(instance=client)

    return render(request,'client/clients_edit.html', {
        'form': form
    })