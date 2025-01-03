import django_filters
from django import forms
from django.db.models import Q
from .models import *
from .forms import getAttrs

class UserFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search', widget=forms.TextInput(attrs=getAttrs('search', 'Rechercher..')))
    new_users_only = django_filters.BooleanFilter(method='filter_new_users', widget=forms.CheckboxInput(attrs={
        'type': 'checkbox',
        'data-onstyle': 'secondary',
        'data-toggle': 'switchbutton',
        'data-onlabel': "Nouveau", 
        'data-offlabel': "Active"
    }))

    def filter_search(self, queryset, name, value):
        return queryset.filter( Q(fullname__icontains=value) | Q(username__icontains=value) | Q(role__icontains=value)).distinct()
    
    def filter_new_users(self, queryset, name, value):
        if value:
            return queryset.filter(role='Nouveau')
        else:
            return queryset.exclude(role='Nouveau')


    class Meta:
        model = User
        fields = ['search', 'new_users_only']

