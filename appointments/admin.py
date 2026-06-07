from django.contrib import admin
from Healthcare_Management.admin import (
    admin_site,
    RoleBasedModelAdmin,
    export_as_csv_action,
    export_as_pdf_action,
)
from .models import Appointment


class AppointmentAdmin(RoleBasedModelAdmin):
    allowed_roles = ['ADMIN', 'DOCTOR', 'RECEPTION']
    add_roles = ['ADMIN', 'RECEPTION']
    change_roles = ['ADMIN', 'RECEPTION']
    delete_roles = ['ADMIN', 'RECEPTION']

    list_display = (
        'id',
        'patient',
        'doctor',
        'appointment_date',
        'appointment_time',
        'status',
        'is_active',
    )
    search_fields = ('patient__name', 'doctor__name')
    list_filter = ('status', 'appointment_date', 'is_active')
    date_hierarchy = 'appointment_date'
    list_per_page = 20
    readonly_fields = ('id',)
    actions = [
        export_as_csv_action('Export selected appointments as CSV'),
        export_as_pdf_action('Export selected appointments as PDF'),
    ]

    def mark_confirmed(self, request, queryset):
        updated = queryset.update(status='CONFIRMED')
        self.message_user(request, f"{updated} appointment(s) marked as confirmed.")
    mark_confirmed.short_description = 'Mark selected appointments as confirmed'

    def mark_completed(self, request, queryset):
        updated = queryset.update(status='COMPLETED')
        self.message_user(request, f"{updated} appointment(s) marked as completed.")
    mark_completed.short_description = 'Mark selected appointments as completed'

    def mark_cancelled(self, request, queryset):
        updated = queryset.update(status='CANCELLED')
        self.message_user(request, f"{updated} appointment(s) marked as cancelled.")
    mark_cancelled.short_description = 'Mark selected appointments as cancelled'

    actions += [mark_confirmed, mark_completed, mark_cancelled]


admin_site.register(Appointment, AppointmentAdmin)
    