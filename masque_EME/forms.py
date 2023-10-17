from django import forms
from .models import Document

class pre40(forms.ModelForm):
    conseiller = forms.CharField(
        max_length=100, 
        required=True, 
        label=('Conseiller'),
        widget=forms.TextInput(attrs={'placeholder': 'NOM, Prénom'})
    )

    mail_conseiller = forms.EmailField(
        max_length=100, 
        required=True, 
        label=('Mail conseiller'),
        widget=forms.TextInput(attrs={'placeholder': 'email@bge-adil.eu'})
    )

    class Meta:
        model = Document # Relates the pre40 class to the Document model in your models
        fields = ['pdf_file'] # Specifies which model
