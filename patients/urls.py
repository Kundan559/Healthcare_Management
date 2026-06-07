from django.urls import path
from . import views

urlpatterns = [
    path(
        '', 
        views.patient_list,
        name= 'patient_list'
        ),
    
    path(
        'add/',
         views.add_patient,
         name='add_patient'
         ),
    
    path(
        'edit/<int:id>',
         views.edit_patient,
         name = 'edit_patient'
         ),
    
    path(
        'detail/<int:id>/',
         views.patient_detail,
         name='patient_detail'
         ),

    path(
        'delete/<int:id>',
         views.delete_patient,
         name = 'delete_patient'
         ),
    path(
        'delete-ajax/<int:id>/',
        views.delete_patient_ajax,
        name='delete_patient_ajax'
        ),
    path(
        'restore-ajax/<int:id>/',
        views.restore_patient_ajax,
        name='restore_patient_ajax'
        ),
    
    path('api/',
         views.patient_list_api,
         name='patient_api'
         ),
    
    path('api/add/',
         views.add_patient_api,
         name='add_patient_api'
         ),
    
    
]