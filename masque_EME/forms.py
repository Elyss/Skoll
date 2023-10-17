from django import forms
from .models import Document

ACTION_CHOICES = [
    ('rdv_diagnostic', 'Rdv de diagnostic'),
    ('atelier_1', 'Atelier 1 - Adéquation individu /idée-projet'),
    ('point_etape_1', 'Point d’étape 1'),
    ('atelier_2', 'Atelier 2 - Cohérence produit-service / Marché'),
    ('point_etape_2', 'Point d’étape 2'),
    ('atelier_3', 'Atelier 3 - Objectif rémunération / Chiffre d’affaires'),
    ('point_etape_3', 'Point d’étape 3'),
    ('rdv_intermediaire', 'Rendez-vous intermédiaire : statuts juridiques'),
    ('atelier_4', 'Atelier 4 - Equilibre besoins / ressources'),
    ('rdv_bilan', 'Rendez-vous de Bilan : création opportune'),
]


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

    rdv_diagnostic = forms.CharField(required=False, max_length=255, label='Rdv de diagnostic')
    atelier_1 = forms.CharField(required=False, max_length=255, label='Atelier 1')
    point_etape_1 = forms.CharField(required=False, max_length=255, label='Point d’étape 1')
    atelier_2 = forms.CharField(required=False, max_length=255, label='Atelier 2')
    point_etape_2 = forms.CharField(required=False, max_length=255, label='Point d’étape 2')
    atelier_3 = forms.CharField(required=False, max_length=255, label='Atelier 3')
    point_etape_3 = forms.CharField(required=False, max_length=255, label='Point d’étape 3')
    rdv_intermediaire = forms.CharField(required=False, max_length=255, label='Rendez-vous intermédiaire')
    atelier_4 = forms.CharField(required=False, max_length=255, label='Atelier 4')
    rdv_bilan = forms.CharField(required=False, max_length=255, label='Rendez-vous de Bilan')

    class Meta:
        model = Document 
        fields = ['pdf_file'] 