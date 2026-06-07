from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.medical_record_list,
        name='medical_record_list'
    ),

    path(
        'add/',
        views.add_medical_record,
        name='add_medical_record'
    ),

]


    
