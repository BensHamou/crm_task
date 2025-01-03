import django_filters
from django import forms
from django.db.models import Q
from .models import *
from .forms import getAttrs

class TaskFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search', widget=forms.TextInput(attrs=getAttrs('search', 'Rechercher..')))

    def filter_search(self, queryset, name, value):
        return queryset.filter( Q(designation__icontains=value)).distinct()

    class Meta:
        model = Task
        fields = ['search']

