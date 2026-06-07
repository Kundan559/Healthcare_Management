from django.db import models

from patients.models import Patient

from appointments.models import Appointment


class Invoice(models.Model):

    STATUS_CHOICES = (

        ('PAID', 'Paid'),

        ('PENDING', 'Pending'),

    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE
    )

    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"Invoice #{self.id}"