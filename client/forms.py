from django import forms

from .models import Client, ClientFile, Comment

class AddClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'email', 'description', 'priority', 'status', 'telefoon_nummer', 'address_1', 'woon_plaats', 'lead_datum',
                   'contact_datum_1', 'contact_datum_2', 'contact_datum_3', 'contact_persoon', 'pakket', 'kvk',)
        
class AddFileForm(forms.ModelForm):
    class Meta:
        model = ClientFile
        fields = ('file',)

class AddCommentForm2(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)