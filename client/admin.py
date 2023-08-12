from django.contrib import admin

from .models import Client, ClientFile

admin.site.register(Client)
admin.site.register(ClientFile)