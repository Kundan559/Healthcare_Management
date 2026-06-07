from django.db import models
from Healthcare_Management.utils import ActiveManager, AllObjectsManager


class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    is_active = models.BooleanField(default=True)

    objects = ActiveManager()
    all_objects = AllObjectsManager()
    
    def __str__(self):
        return self.name
# Create your models here.
