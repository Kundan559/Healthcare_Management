import csv
import json
import textwrap
from datetime import date

from django.contrib import admin, messages
from django.contrib.admin import AdminSite
from django.db.models import Count
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.translation import gettext_lazy as _

from accounts.models import UserRole
from appointments.models import Appointment
from doctors.models import Doctor
from patients.models import Patient
from records.models import AuditLog
from django.contrib import messages


def get_user_role(user):
    if not user.is_authenticated:
        return None

    if user.is_superuser:
        return 'SUPERUSER'

    try:
        return UserRole.objects.get(user=user).role
    except UserRole.DoesNotExist:
        return None


def has_role(user, allowed_roles):
    if user.is_superuser:
        return True
    role = get_user_role(user)
    return bool(role and role in allowed_roles)


def export_as_csv_action(description="Export selected records as CSV"):
    def export_as_csv(modeladmin, request, queryset):
        meta = modeladmin.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f"attachment; filename={meta.verbose_name_plural}.csv"
        writer = csv.writer(response)
        writer.writerow(field_names)

        for obj in queryset:
            row = []
            for field in field_names:
                value = getattr(obj, field, "")
                if value is None:
                    value = ""
                row.append(str(value))
            writer.writerow(row)

        return response

    export_as_csv.short_description = description
    return export_as_csv


def export_as_pdf_action(description="Export selected records as PDF"):

    def export_as_pdf(modeladmin, request, queryset):

        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas

        except ImportError:

            modeladmin.message_user(
                request,
                "PDF export requires the ReportLab package.",
                level=messages.ERROR,
            )

            return None

        meta = modeladmin.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f"attachment; filename={meta.verbose_name_plural}.pdf"

        pdf = canvas.Canvas(response, pagesize=letter)
        width, height = letter
        y = height - 40
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(40, y, f"{meta.verbose_name_plural.title()} Report")
        y -= 25
        pdf.setFont("Helvetica", 10)

        pdf.drawString(40, y, " | ".join(field_names))
        y -= 15

        for obj in queryset:
            row = " | ".join(str(getattr(obj, field, "")) for field in field_names)
            lines = textwrap.wrap(row, 120)
            for line in lines:
                if y < 60:
                    pdf.showPage()
                    y = height - 40
                    pdf.setFont("Helvetica", 10)
                pdf.drawString(40, y, line)
                y -= 14

        pdf.showPage()
        pdf.save()
        return response

    export_as_pdf.short_description = description
    return export_as_pdf


class RoleBasedModelAdmin(admin.ModelAdmin):
    allowed_roles = ['ADMIN']
    add_roles = None
    change_roles = None
    delete_roles = None
    view_roles = None

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        roles = self.view_roles if self.view_roles is not None else self.allowed_roles
        return has_role(request.user, roles)

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        roles = self.add_roles if self.add_roles is not None else self.allowed_roles
        return has_role(request.user, roles)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        roles = self.change_roles if self.change_roles is not None else self.allowed_roles
        return has_role(request.user, roles)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        roles = self.delete_roles if self.delete_roles is not None else self.allowed_roles
        return has_role(request.user, roles)


class HealthcareAdminSite(AdminSite):
    site_header = "Healthcare Management Admin"
    site_title = "HMS Admin Portal"
    index_title = "Healthcare Management Dashboard"
    index_template = "admin/index.html"

    def has_permission(self, request):
        if not request.user.is_active or not request.user.is_staff:
            return False
        return has_role(request.user, ['ADMIN', 'RECEPTION', 'DOCTOR'])

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('user-role/', self.admin_view(self.user_role_view), name='user_role_view'),
        ]
        return custom_urls + urls

    def user_role_view(self, request):
        user_role = get_user_role(request.user)
        return HttpResponse(f"Your admin role is: {user_role}")

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        today = date.today()
        appointment_status = Appointment.objects.values('status').order_by('status').annotate(count=Count('id'))
        appointment_status_counts = {item['status']: item['count'] for item in appointment_status}
        appointment_trend = (
            Appointment.objects.filter(appointment_date__gte=today)
            .values('appointment_date')
            .order_by('appointment_date')
            .annotate(count=Count('id'))
        )
        recent_logs = AuditLog.objects.order_by('-timestamp')[:5]

        extra_context.update({
            'patient_count': Patient.objects.filter(is_active=True).count(),
            'doctor_count': Doctor.objects.filter(is_active=True).count(),
            'appointment_count': Appointment.objects.filter(is_active=True).count(),
            'pending_count': appointment_status_counts.get('PENDING', 0),
            'confirmed_count': appointment_status_counts.get('CONFIRMED', 0),
            'completed_count': appointment_status_counts.get('COMPLETED', 0),
            'cancelled_count': appointment_status_counts.get('CANCELLED', 0),
            'appointment_status_counts': json.dumps(appointment_status_counts),
            'appointment_date_labels': json.dumps([item['appointment_date'].isoformat() for item in appointment_trend]),
            'appointment_date_counts': json.dumps([item['count'] for item in appointment_trend]),
            'recent_logs': recent_logs,
        })
        return super().index(request, extra_context)


admin_site = HealthcareAdminSite(name='healthcare_admin')

# Register the admin site with built-in models so custom headers apply
admin.site = admin_site
