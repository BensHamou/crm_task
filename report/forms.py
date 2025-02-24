from account.forms import BaseModelForm, getAttrs
from .models import *
from django import forms

class TaskForm(BaseModelForm):
    class Meta:
        model = Task
        fields = ['designation', 'commercial', 'comm_team', 'task_type', 'project', 'lead', 'client', 'wilaya', 
                  'project_id', 'lead_id', 'client_id', 'date_task', 'date_done', 'description', 'resume', 'google_maps_coords']
        

    designation = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlReq', 'Désignation')))
    commercial = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(attrs=getAttrs('select2', 'Commercial')))
    date_task = forms.DateTimeField(widget=forms.DateTimeInput(attrs=getAttrs('dateReq'), format='%Y-%m-%d'))
    date_done = forms.DateTimeField(widget=forms.DateTimeInput(attrs=getAttrs('date'), format='%Y-%m-%d'), required=False)
    comm_team = forms.ModelChoiceField(queryset=CRMTeam.objects.all(), widget=forms.Select(attrs=getAttrs('select2', 'Équipe commerciale')))
    task_type = forms.ModelChoiceField(queryset=TaskType.objects.all(), widget=forms.Select(attrs=getAttrs('select2', 'Type de tâche')))
    wilaya = forms.ModelChoiceField(queryset=Wilaya.objects.all(), widget=forms.Select(attrs=getAttrs('select2', 'Wilaya')))

    project = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlSearch', 'Projet')), required=False)
    lead = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlSearch', 'Piste')), required=False)
    client = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlSearch', 'Client, prospect ou contact')), required=False)

    project_id = forms.IntegerField(widget=forms.HiddenInput(attrs=getAttrs('controlIDReq','ID du projet')), required=False)
    lead_id = forms.IntegerField(widget=forms.HiddenInput(attrs=getAttrs('controlIDReq','ID du piste')), required=False)
    client_id = forms.IntegerField(widget=forms.HiddenInput(attrs=getAttrs('controlIDReq','ID du client')), required=False)

    description = forms.CharField(widget=forms.Textarea(attrs=getAttrs('textareaReq', 'Description')))
    resume = forms.CharField(widget=forms.Textarea(attrs=getAttrs('textarea', 'Résumé')), required=False)
    google_maps_coords = forms.CharField(widget=forms.HiddenInput(attrs=getAttrs('control', 'Coordonnées Google Maps')), required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['commercial'].initial = user
        self.fields['comm_team'].queryset = CRMTeam.objects.filter(id__in=user.teams.all().values_list('id', flat=True))

        if user.has_leader():
            self.fields['commercial'].queryset = User.objects.filter(teams__in=user.teams.all()).distinct()
        else:
            self.fields['commercial'].queryset = User.objects.filter(id=user.id)
            self.fields['commercial'].widget.attrs['disabled'] = True


class ImageForm(BaseModelForm):
    class Meta:
        model = Image
        fields = ['image']

    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'custom-file-input','accept': 'image/*'}))