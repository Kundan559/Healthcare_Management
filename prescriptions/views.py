from django.shortcuts import render, redirect

from .models import Prescription

from .forms import PrescriptionForm


def prescription_list(request):

    prescriptions = Prescription.objects.all()

    return render(

        request,

        'prescriptions/prescription_list.html',

        {

            'prescriptions': prescriptions

        }
    )


def add_prescription(request):

    if request.method == 'POST':

        form = PrescriptionForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('prescription_list')

    else:

        form = PrescriptionForm()

    return render(

        request,

        'prescriptions/add_prescription.html',

        {

            'form': form

        }
    )
# Create your views here.
