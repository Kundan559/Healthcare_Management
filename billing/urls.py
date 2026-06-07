from django.urls import path

from . import views


urlpatterns = [
    
    path(
        '',
        views.billing_list,
        name='billing_list'
    ),

    path(
        '',
        views.invoice_list,
        name='invoice_list'
    ),

    path(
        'add/',
        views.add_invoice,
        name='add_invoice'
    ),

]