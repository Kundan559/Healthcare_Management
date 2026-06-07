from django import forms

from .models import LabReport


class LabReportForm(forms.ModelForm):

    class Meta:

        model = LabReport

        fields = '__all__'