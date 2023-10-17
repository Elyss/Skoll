# authentication/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='Mail BGE')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Mot de passe')


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(
        label="Mot de passe",
        strip=False,
        widget=forms.PasswordInput,
    )
    
    password2 = forms.CharField(
        label="Confirmation du mot de passe",
        widget=forms.PasswordInput,
        strip=False,
    )
    
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name')
        labels = {
            'email': 'Email BGE',
            'first_name': 'Prénom',
            'last_name': 'NOM',
            'password':"Mot de passe",
        }