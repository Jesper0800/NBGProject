from django import forms

from .models import Lead,Comment

class AddLeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ('name', 'email', 'description', 'priority', 'status', 'telefoon_nummer', 'address_1', 'woon_plaats', 'lead_datum',
                   'contact_datum_1', 'contact_datum_2', 'contact_datum_3', 'contact_persoon','contact_persoon_email', 'pakket', 'kvk', 'belasting_nummer',)
        
class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)