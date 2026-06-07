from django.db import models
from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment
# Create your models here.

class Prescription(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        
    )
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
    )

    medicines = models.TextField()

    diagnosis = models.TextField()

    notes = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.patient.name}"
    
class Diagnosis(models.Model):

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE
    )

    diagnosis = models.TextField()

    diagnosis_date = models.DateField()    
