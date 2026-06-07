from django.urls import path
from . import views

urlpatterns = [
    path(
        '',
        views.doctor_list, 
        name='doctor_list'
        ),
    path(
        'add/',
        views.add_doctor,
        name='add_doctor'
        ),
    path(
        'edit/<int:id>/',
        views.edit_doctor,
        name='edit_doctor'
        ),
    path(
        'detail/<int:id>/',
        views.doctor_detail,
        name='doctor_detail'
        ),
    path(
        'delete/<int:id>/',
        views.delete_doctor,
        name='delete_doctor'
        ),
    path(
        'delete-ajax/<int:id>/',
        views.delete_doctor_ajax,
        name='delete_doctor_ajax'
        ),
    path(
        'restore-ajax/<int:id>/',
        views.restore_doctor_ajax,
        name='restore_doctor_ajax'
        ),
]
