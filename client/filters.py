import django_filters
from .models import *

class ClientFilter(django_filters.FilterSet):
    class Meta:
        model = Client
        fields = '__all__'