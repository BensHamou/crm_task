from account.forms import BaseModelForm, getAttrs
from .models import *
from django import forms

class TaskForm(BaseModelForm):
    class Meta:
        model = Task
        fields = ['designation', 'comm_team', 'task_type', 'project', 'lead', 'client', 'wilaya', 
                  'task_type_id', 'project_id', 'lead_id', 'client_id', 'wilaya_id', 
                  'date_task', 'description', 'resume', 'google_maps_coords']
        

    designation = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlReq', 'Désignation')))
    date_task = forms.DateTimeField(widget=forms.DateTimeInput(attrs=getAttrs('dateReq'), format='%Y-%m-%d'))
    comm_team = forms.ModelChoiceField(queryset=CRMTeam.objects.all(), widget=forms.Select(attrs=getAttrs('select2', 'Équipe commerciale')))

    task_type = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlSearchReq', 'Type de tâche')))
    project = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlSearch', 'Projet')), required=False)
    lead = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlSearch', 'Piste')), required=False)
    client = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlSearch', 'Client, prospect ou contact')), required=False)
    wilaya = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlSearchReq', 'Wilaya')))

    task_type_id = forms.IntegerField(widget=forms.HiddenInput(attrs=getAttrs('controlIDReq','ID de type de tâche')))
    project_id = forms.IntegerField(widget=forms.HiddenInput(attrs=getAttrs('controlIDReq','ID du projet')), required=False)
    lead_id = forms.IntegerField(widget=forms.HiddenInput(attrs=getAttrs('controlIDReq','ID du piste')), required=False)
    client_id = forms.IntegerField(widget=forms.HiddenInput(attrs=getAttrs('controlIDReq','ID du client')), required=False)
    wilaya_id = forms.IntegerField(widget=forms.HiddenInput(attrs=getAttrs('controlIDReq','ID du wilaya')))

    description = forms.CharField(widget=forms.Textarea(attrs=getAttrs('textarea', 'Description')), required=False)
    resume = forms.CharField(widget=forms.Textarea(attrs=getAttrs('textarea', 'Résumé')), required=False)
    google_maps_coords = forms.CharField(widget=forms.HiddenInput(attrs=getAttrs('control', 'Coordonnées Google Maps')), required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['comm_team'].queryset = CRMTeam.objects.filter(id__in=user.teams.all().values_list('id', flat=True))


class ImageForm(BaseModelForm):
    class Meta:
        model = Image
        fields = ['image']

    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'custom-file-input','accept': 'image/*'}))