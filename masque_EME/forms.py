from django import forms
from .models import Document

class pre40(forms.ModelForm):
   class Meta:
        model = Document
        fields = ['pdf_file']
