from django.shortcuts import render, redirect

from .models import Invoice

from .forms import InvoiceForm




def billing_list(request):

    return render(
        request,
        'billing/billing_list.html'
    )
    
    
def invoice_list(request):

    invoices = Invoice.objects.all()

    return render(

        request,

        'billing/invoice_list.html',

        {

            'invoices': invoices

        }
    )


def add_invoice(request):

    if request.method == 'POST':

        form = InvoiceForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('invoice_list')

    else:

        form = InvoiceForm()

    return render(

        request,

        'billing/add_invoice.html',

        {

            'form': form

        }
    )