from django.template.defaultfilters import slugify
from PIL import Image as PILImage
from django.db import models
from account.models import *
import os

class Task(BaseModel):
        
    STATE_TASK = [
        ('A Faire', 'A Faire'),
        ('Fait', 'Fait')
    ]

    commercial = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    comm_team = models.ForeignKey(CRMTeam, on_delete=models.CASCADE, related_name='tasks')
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE, related_name='tasks')
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE, related_name='tasks')

    designation = models.CharField(max_length=50)

    client_id = models.IntegerField(blank=True, null=True)
    client = models.CharField(max_length=255, blank=True, null=True)

    project_id = models.IntegerField(blank=True, null=True)
    project = models.CharField(max_length=255, blank=True, null=True)

    lead_id = models.IntegerField(blank=True, null=True)
    lead = models.CharField(max_length=255, blank=True, null=True)

    date_task = models.DateTimeField(blank=True, null=True)
    date_done = models.DateTimeField(blank=True, null=True)

    description = models.TextField(blank=True, null=True)
    resume = models.TextField(blank=True, null=True)
    google_maps_coords = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=50, choices=STATE_TASK, default='A Faire')


    def __str__(self):
        return self.designation
    
def get_image_filename(instance, filename):
    title = instance.task.designation
    slug = slugify(title)
    return f'task_images/{slug}-{filename}'

class Image(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=get_image_filename, verbose_name='Image')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image and os.path.exists(self.image.path):
            img = PILImage.open(self.image.path)
            max_size = (1280, 720)
            img.thumbnail(max_size, PILImage.LANCZOS)
            img.save(self.image.path, quality=50, optimize=True)