from django import forms

from .models import Prescription


class PrescriptionForm(forms.ModelForm):

    class Meta:

        model = Prescription

        fields = '__all__'

        widgets = {

            'medicines': forms.Textarea(
                attrs={'rows': 4}
            ),

            'diagnosis': forms.Textarea(
                attrs={'rows': 4}
            ),

            'notes': forms.Textarea(
                attrs={'rows': 3}
            ),

        }