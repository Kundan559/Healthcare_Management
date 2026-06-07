from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import date
from django.db.models import Count

from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment

from accounts.models import UserRole

@login_required
def dashboard(request):

    role = UserRole.objects.filter(
        user=request.user
    ).first()
    # Safely handle cases where no UserRole record exists for the user
    role_value = role.role if role and getattr(role, 'role', None) else 'Staff'

    today = date.today()
    appointments = Appointment.objects.all()

    # Use the reverse relation lookup name, not the Python accessor name.
    # Django reverse lookup for a ForeignKey uses the model name by default.
    top_doctors = Doctor.objects.annotate(
        appointment_count=Count('appointments')
    ).order_by('-appointment_count')[:5]

    context = {
        'role': role_value,
        'total_patients': Patient.objects.count(),
        'total_doctors': Doctor.objects.count(),
        'total_appointments': appointments.count(),
        'pending_appointments': appointments.filter(status='PENDING').count(),
        'confirmed_appointments': appointments.filter(status='CONFIRMED').count(),
        'completed_appointments': appointments.filter(status='COMPLETED').count(),
        'today_appointments': appointments.filter(appointment_date=today).count(),
        'upcoming_appointments': appointments.filter(appointment_date__gte=today).order_by('appointment_date', 'appointment_time')[:5],
        'top_doctors': top_doctors,
        'recent_appointments': appointments.order_by('-appointment_date', '-appointment_time')[:5],
    }

    return render(
        request,
        'dashboard/dashboard.html',
        context
    )