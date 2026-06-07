from django.contrib import admin
from Healthcare_Management.admin import (
    admin_site,
    RoleBasedModelAdmin,
    export_as_csv_action,
    export_as_pdf_action,
)
from .models import Patient
from appointments.models import Appointment


class AppointmentInline(admin.TabularInline):
    model = Appointment
    fk_name = 'patient'
    fields = ('doctor', 'appointment_date', 'appointment_time', 'status', 'is_active')
    readonly_fields = ('doctor', 'appointment_date', 'appointment_time', 'status')
    extra = 0
    show_change_link = True


class PatientAdmin(RoleBasedModelAdmin):
    allowed_roles = ['ADMIN', 'DOCTOR', 'RECEPTION']
    add_roles = ['ADMIN', 'RECEPTION']
    change_roles = ['ADMIN', 'RECEPTION']
    delete_roles = ['ADMIN', 'RECEPTION']

    list_display = ('id', 'name', 'age', 'gender', 'phone', 'is_active')
    search_fields = ('name', 'phone')
    list_filter = ('gender', 'is_active')
    ordering = ('name',)
    list_per_page = 15
    inlines = [AppointmentInline]
    actions = [
        export_as_csv_action('Export selected patients as CSV'),
        export_as_pdf_action('Export selected patients as PDF'),
    ]


admin_site.register(Patient, PatientAdmin)
