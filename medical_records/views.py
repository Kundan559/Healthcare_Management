from django.shortcuts import render, redirect

from .models import MedicalRecord

from .forms import MedicalRecordForm


def medical_record_list(request):

    records = MedicalRecord.objects.all()

    return render(

        request,

        'medical_records/record_list.html',

        {

            'records': records

        }
    )


def add_medical_record(request):

    if request.method == 'POST':

        form = MedicalRecordForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect('medical_record_list')

    else:

        form = MedicalRecordForm()

    return render(

        request,

        'medical_records/add_record.html',

        {

            'form': form

        }
    )