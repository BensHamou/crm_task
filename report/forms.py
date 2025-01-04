from account.forms import BaseModelForm, getAttrs
from .models import *
from django import forms

class TaskForm(BaseModelForm):
    class Meta:
        model = Task
        fields = ['designation', 'comm_team', 'task_type', 'project', 'lead', 'client', 'wilaya', 
                  'comm_team_id', 'task_type_id', 'project_id', 'lead_id', 'client_id', 'wilaya_id', 
                  'date_task', 'date_scheduler', 'date_done', 'delais_late', 'description', 'resume', 'google_maps_coords']

    designation = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlReq', 'Désignation')))

    comm_team = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlSearchReq', 'Equipe Commerciale')))
    task_type = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlSearchReq', 'Type de tâche')))
    project = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlSearch', 'Projet')), required=False)
    lead = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlSearch', 'Piste')), required=False)
    client = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlSearch', 'Client, prospect ou contact')), required=False)
    wilaya = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlSearchReq', 'Wilaya')))

    comm_team_id = forms.IntegerField(widget=forms.HiddenInput(attrs=getAttrs('controlIDReq','ID de l\'équipe de communication')))
    task_type_id = forms.IntegerField(widget=forms.HiddenInput(attrs=getAttrs('controlIDReq','ID de type de tâche')))
    project_id = forms.IntegerField(widget=forms.HiddenInput(attrs=getAttrs('controlIDReq','ID du projet')), required=False)
    lead_id = forms.IntegerField(widget=forms.HiddenInput(attrs=getAttrs('controlIDReq','ID du piste')), required=False)
    client_id = forms.IntegerField(widget=forms.HiddenInput(attrs=getAttrs('controlIDReq','ID du client')), required=False)
    wilaya_id = forms.IntegerField(widget=forms.HiddenInput(attrs=getAttrs('controlIDReq','ID du wilaya')))

    date_task = forms.DateTimeField(widget=forms.DateTimeInput(attrs=getAttrs('dateReq'), format='%Y-%m-%d'))
    date_scheduler = forms.DateTimeField(widget=forms.DateTimeInput(attrs=getAttrs('date'), format='%Y-%m-%d'), required=False)
    date_done = forms.DateTimeField(widget=forms.DateTimeInput(attrs=getAttrs('date'), format='%Y-%m-%d'), required=False)
    delais_late = forms.DateTimeField(widget=forms.DateTimeInput(attrs=getAttrs('date'), format='%Y-%m-%d'), required=False)

    description = forms.CharField(widget=forms.Textarea(attrs=getAttrs('textarea', 'Description')), required=False)
    resume = forms.CharField(widget=forms.Textarea(attrs=getAttrs('textarea', 'Résumé')), required=False)
    google_maps_coords = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control', 'Coordonnées Google Maps')), required=False)


class ImageForm(BaseModelForm):
    class Meta:
        model = Image
        fields = ['image']

    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'custom-file-input','accept': 'image/*'}))