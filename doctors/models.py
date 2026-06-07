from django.db import models
from Healthcare_Management.utils import ActiveManager, AllObjectsManager


class Doctor(models.Model):

    SPECIALIZATION_CHOICES = (

    ('Cardiology', 'Cardiology'),

    ('Neurology', 'Neurology'),

    ('Orthopedics', 'Orthopedics'),

    ('Dermatology', 'Dermatology'),

    ('Pediatrics', 'Pediatrics'),

    ('Gynecology', 'Gynecology'),

    ('Psychiatry', 'Psychiatry'),

    ('Oncology', 'Oncology'),

    ('Radiology', 'Radiology'),

    ('General Medicine', 'General Medicine'),

    ('ENT', 'ENT'),

    ('Ophthalmology', 'Ophthalmology'),

    ('Urology', 'Urology'),

    ('Gastroenterology', 'Gastroenterology'),

    ('Pulmonology', 'Pulmonology'),

    ('Nephrology', 'Nephrology'),

    ('Endocrinology', 'Endocrinology'),

    ('Anesthesiology', 'Anesthesiology'),

    ('Emergency Medicine', 'Emergency Medicine'),

    ('Physiotherapy', 'Physiotherapy'),

)

    name = models.CharField(max_length=100)

    specialization = models.CharField(
        max_length=50,
        choices=SPECIALIZATION_CHOICES
    )

    phone = models.CharField(max_length=15)

    email = models.EmailField(
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    objects = ActiveManager()

    all_objects = AllObjectsManager()

    def __str__(self):

        return self.name
    
    def __str__(self):
        return self.name

