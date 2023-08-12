from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from lead.models import Lead
from client.models import Client

@login_required
def dashboard(request):
    leads = Lead.objects.filter(converted_to_client=False).order_by('created_at',)[0:5]
    clients = Client.objects.order_by('created_at',)[0:5]
    return render(request, 'template/dashboard.html',{
        'leads':leads,
        'clients':clients
    })