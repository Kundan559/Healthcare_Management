from django.shortcuts import render, redirect

from .models import Insurance

from .forms import InsuranceForm


def insurance_list(request):

    insurances = Insurance.objects.all()

    return render(

        request,

        'insurance/insurance_list.html',

        {

            'insurances': insurances

        }
    )


def add_insurance(request):

    if request.method == 'POST':

        form = InsuranceForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('insurance_list')

    else:

        form = InsuranceForm()

    return render(

        request,

        'insurance/add_insurance.html',

        {

            'form': form

        }
    )