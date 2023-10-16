from django import forms
from .models import Document

class pre40(forms.ModelForm):
   class Meta:
        model = Document # Relie la classe pre40 au modèle Document dans mes modèles
        fields = ['pdf_file'] # Précise quels champs du modèle doivent être inclus à ce formulaire
