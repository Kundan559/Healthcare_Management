from django.urls import path
from . import views

urlpatterns = [
    path(
        '',
        views.appointment_list,
        name='appointment_list'
        ),
    
    path(
        'add/',
        views.add_appointment,
        name='add_appointment'
        ),
    
    path(
        'edit/<int:id>/',
        views.edit_appointment,
        name='edit_appointment'
        ),
    path(
        'detail/<int:id>/',
        views.appointment_detail,
        name='appointment_detail'
        ),
    
    path(
        'delete/<int:id>/',
        views.delete_appointment,
        name='delete_appointment'
        ),
    path(
        'delete-ajax/<int:id>/',
        views.delete_appointment_ajax,
        name='delete_appointment_ajax'
        ),
    path(
        'restore-ajax/<int:id>/',
        views.restore_appointment_ajax,
        name='restore_appointment_ajax'
        ),
    
    path(
        'confirm/<int:pk>/',
        views.confirm_appointment,
        name='confirm_appointment'
        ),
    path(
        'confirm-ajax/<int:pk>/',
        views.confirm_appointment_ajax,
        name='confirm_appointment_ajax'
        ),
    
    path(
        'complete/<int:pk>/',
        views.complete_appointment,
        name='complete_appointment'
        ),
    path(
        'complete-ajax/<int:pk>/',
        views.complete_appointment_ajax,
        name='complete_appointment_ajax'
        ),
    
    path(
        'cancel/<int:pk>/',
        views.cancel_appointment,
        name='cancel_appointment'
        ),
    path(
        'cancel-ajax/<int:pk>/',
        views.cancel_appointment_ajax,
        name='cancel_appointment_ajax'
        ),
]
