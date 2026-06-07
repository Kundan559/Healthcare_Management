from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.insurance_list,
        name='insurance_list'
    ),

    path(
        'add/',
        views.add_insurance,
        name='add_insurance'
    ),

]