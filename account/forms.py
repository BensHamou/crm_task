from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from datetime import datetime
from django import forms
from .models import *
from django import forms

def getAttrs(type, placeholder='', other={}):
    ATTRIBUTES = {
        'control': {'class': 'form-control', 'style': 'background-color: #ffffff; padding-left: 30px; border-radius: 100px;', 'placeholder': ''},
        'login': {'class': 'form-control', 'style': 'padding-left: 30px; background-color: white; height: 45px; border: 1px solid #ccc; border-radius: 100px;', 'placeholder': ''},
        'controlID': {'class': 'form-control search-input-id', 'autocomplete': "off", 'style': 'background-color: #ffffff; padding-left: 30px; border-radius: 100px;', 'placeholder': ''},
        'controlSearch': {'class': 'form-control search-input', 'autocomplete': "off", 'style': 'background-color: #ffffff; padding-left: 30px; border-radius: 100px;', 'placeholder': ''},
        'search': {'class': 'form-control mb-lg-0 mb-3', 'style': 'padding-left: 30px; margin-right: 10px; border-radius: 100px; max-width: 500px', 'type': 'text', 'placeholder': '', 'id': 'search'},
        'select': {'class': 'form-select', 'style': 'background-color: #ffffff; padding-left: 30px; border-radius: 100px;'},
        'select2': {'class': 'form-select select2', 'style': 'background-color: #ffffff; padding-left: 30px; width: 100%; border-radius: 100px;'},
        'select3': {'class': 'form-select select3', 'style': 'background-color: #ffffff; padding-left: 30px; width: 100%; border-radius: 100px;'},
        'date': {'type': 'date', 'class': 'form-control dateinput','style': 'background-color: #ffffff; padding-left: 30px; border-radius: 100px;'},
        'time': {'type': 'time', 'class': 'form-control timeinput', 'style': 'background-color: #ffffff; padding-left: 30px; border-radius: 100px;', 'placeholder': ''},
        'month': {'type': 'month', 'class': 'form-control dateinput','style': 'background-color: #ffffff; padding-left: 30px; border-radius: 100px;'},
        'textarea': {"rows": "3", 'style': 'width: 100%', 'class': 'form-control', 'placeholder': '', 'style': 'padding-left: 30px; background-color: #ffffff; border-radius: 50px;'}
    }

    if type in ATTRIBUTES:
        attributes = ATTRIBUTES[type]
        if 'placeholder' in attributes:
            attributes['placeholder'] = placeholder
        if other:
            attributes.update(other)
        return attributes
    else:
        return {}
    
class BaseModelForm(ModelForm):
    def save(self, commit=True, user=None):
        instance = super(BaseModelForm, self).save(commit=False)
        if user:
            if not instance.pk:
                instance.create_uid = user
            instance.write_uid = user
        if commit:
            instance.save()
        return instance
    
class UserForm(BaseModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_admin', 'first_name', 'last_name', 'role']

    username = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control', 'Nom d\'utilisateur')), disabled=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control', 'Nom de famille')), disabled=True)
    first_name = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control', 'Prénom')), disabled=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs=getAttrs('control', 'Email')), disabled=True)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, widget=forms.Select(attrs=getAttrs('select')))
    is_admin = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'type': 'checkbox',
        'data-onstyle': 'primary',
        'data-toggle': 'switchbutton',
        'data-onlabel': "Admin", 
        'data-offlabel': "User"
    }))
    
class CustomLoginForm(AuthenticationForm):
    
    username = forms.CharField(label="Email / AD 2000", widget=forms.TextInput(attrs=getAttrs('login', 'Adresse e-mail', {'autofocus': True})))
    password = forms.CharField(widget=forms.PasswordInput(attrs=getAttrs('login', 'Mot de passe')))
