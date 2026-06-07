from django.db import models
from patients.models import Patient

# Create your models here.
class Insurance(models.Model):

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE
    )

    provider_name = models.CharField(
        max_length=100
    )

    policy_number = models.CharField(
        max_length=100
    )
    
    valid_till = models.DateField()

    # coverage_details = models.TextField()

    # valid_from = models.DateField()

    # valid_to = models.DateField()

    def __str__(self):

        return f"{self.patient.name} - {self.provider_name}"

