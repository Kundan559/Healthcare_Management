from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.lab_report_list,
        name='lab_report_list'
    ),

    path(
        'add/',
        views.add_lab_report,
        name='add_lab_report'
    ),

]