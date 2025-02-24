from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    create_uid = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="created_%(class)s", on_delete=models.SET_NULL, null=True, blank=True)
    write_uid = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="modified_%(class)s", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        abstract = True

class Setting(BaseModel):
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.name} : {self.value}"

class CRMTeam(BaseModel):
    name = models.CharField(max_length=50)
    odoo_id = models.IntegerField(default=0)
    def __str__(self):
        return self.name

class Wilaya(BaseModel):
    name = models.CharField(max_length=50)
    odoo_id = models.IntegerField(default=0)
    def __str__(self):
        return self.name

class TaskType(BaseModel):
    name = models.CharField(max_length=50)
    odoo_id = models.IntegerField(default=0)
    def __str__(self):
        return self.name
    
class User(BaseModel, AbstractUser):
    ROLE_CHOICES = [
        ('Nouveau', 'Nouveau'),
        ('Commercial', 'Commercial'),
        ('Chef équipe', 'Chef équipe'),
        ('Observateur', 'Observateur'),
        ('Admin', 'Admin')
    ]

    fullname = models.CharField(max_length=255)
    role = models.CharField(choices=ROLE_CHOICES, max_length=30)
    is_admin = models.BooleanField(default=False)
    teams = models.ManyToManyField(CRMTeam, related_name='users', blank=True)


    def __str__(self):
        return self.fullname
    
    def has_admin(self):
        return self.role == 'Admin'
    
    def has_leader(self):
        return self.role in ['Admin', 'Chef équipe']
    
    def has_commercial(self):
        return self.role in ['Commercial', 'Chef équipe']
    
    def has_obs(self):
        return self.role == 'Observateur'

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
