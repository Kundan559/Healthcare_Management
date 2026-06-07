from django.shortcuts import render, redirect

from .models import LabReport

from .forms import LabReportForm


def lab_report_list(request):

    reports = LabReport.objects.all()

    return render(

        request,

        'lab_reports/report_list.html',

        {

            'reports': reports

        }
    )


def add_lab_report(request):

    if request.method == 'POST':

        form = LabReportForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect('lab_report_list')

    else:

        form = LabReportForm()

    return render(

        request,

        'lab_reports/add_report.html',

        {

            'form': form

        }
    )