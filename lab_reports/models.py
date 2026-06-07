from django.db import models

from patients.models import Patient


class LabReport(models.Model):

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE
    )

    report_type = models.CharField(
        max_length=100
    )

    result = models.TextField()

    report_file = models.FileField(
        upload_to='lab_reports/'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.report_type