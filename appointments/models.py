from django.db import models
from patients.models import Patient
from doctors.models import Doctor
from Healthcare_Management.utils import ActiveManager, AllObjectsManager


class Appointment(models.Model):

    STATUS_CHOICES = (

        ('PENDING', 'Pending'),

        ('CONFIRMED', 'Confirmed'),

        ('COMPLETED', 'Completed'),

        ('CANCELLED', 'Cancelled'),

    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    appointment_date = models.DateField()

    appointment_time = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    is_active = models.BooleanField(default=True)

    objects = ActiveManager()
    all_objects = AllObjectsManager()

    def __str__(self):

        return f"{self.patient} - {self.doctor}"
    
    
