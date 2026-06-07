from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Doctor
from .forms import DoctorForm
from appointments.models import Appointment
from datetime import date
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from accounts.decorators import allowed_users

# Create your views here.

@login_required
@allowed_users(['ADMIN', 'DOCTOR', 'RECEPTION'])
def doctor_list(request):
    query = request.GET.get('q')
    specialization = request.GET.get('specialization')

    doctors = Doctor.objects.all().order_by('id')

    if query:
        doctors = doctors.filter(
            Q(name__icontains=query) | Q(specialization__icontains=query)
        )

    if specialization:
        doctors = doctors.filter(specialization__iexact=specialization)

    specializations = (
    Doctor.objects
    .order_by('specialization')
    .values_list(
        'specialization',
        flat=True
    )
    .distinct()
    )

    paginator = Paginator(doctors, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'doctors': page_obj,
        'specializations': specializations,
        'page_obj': page_obj,
    }

    return render(
        request,
        'doctors/doctor_list.html',
        context
    )

# Doctor Detail
@login_required
@allowed_users(['ADMIN', 'DOCTOR', 'RECEPTION'])
def doctor_detail(request,id):
    doctor = get_object_or_404(Doctor, id=id)
    appointments = Appointment.objects.filter(doctor=doctor)
    upcoming_appointments = appointments.filter(appointment_date__gte=date.today()).count()
    next_appointment = appointments.filter(appointment_date__gte=date.today()).order_by('appointment_date', 'appointment_time').first()

    return render(
        request,
        'doctors/doctor_detail.html',
        {
            'doctor': doctor,
            'appointment_count': appointments.count(),
            'upcoming_appointments': upcoming_appointments,
            'next_appointment': next_appointment,
            'recent_appointments': appointments.order_by('-appointment_date', '-appointment_time')[:3],
        }
    )

# Add Doctor
@login_required
@allowed_users(['ADMIN', 'RECEPTION'])
def add_doctor(request):
    if request.method == "POST" :
        form = DoctorForm(request.POST)
        
        
        if form.is_valid():
            form.save()
            return redirect('doctor_list')
            
    else:
        form = DoctorForm()
            
    return render(
        request,
        'doctors/add_doctor.html',
        {'form':form}
    )
        
# Edit Doctor
@login_required
@allowed_users(['ADMIN', 'RECEPTION'])
def edit_doctor(request,id):
    doctor = get_object_or_404(Doctor,id=id)
    
    if request.method == "POST":
        form = DoctorForm(
            request.POST, instance=doctor
        )
        
        if form.is_valid():
            form.save()
            return redirect('doctor_list')
            
    else:
        form = DoctorForm(instance=doctor)
            
    return render(
        request,
        'doctors/edit_doctor.html',
        {'form':form}
    )
        
# Delete Doctor
@login_required
@allowed_users(['ADMIN', 'RECEPTION'])
def delete_doctor(request,id):
    doctor = get_object_or_404(Doctor,id=id)
    # Prefer soft-delete to allow undo
    doctor.is_active = False
    doctor.save()
    return redirect('doctor_list')


@login_required
@allowed_users(['ADMIN', 'RECEPTION'])
def delete_doctor_ajax(request, id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        doctor = get_object_or_404(Doctor, id=id)
        doctor.is_active = False
        doctor.save()
        undo_url = reverse('restore_doctor_ajax', args=[id])
        return JsonResponse({'success': True, 'id': id, 'undo_url': undo_url, 'message': 'Doctor deleted.'})
    return JsonResponse({'success': False}, status=400)


@login_required
@allowed_users(['ADMIN', 'RECEPTION'])
def restore_doctor_ajax(request, id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        doctor = get_object_or_404(Doctor.all_objects, id=id)
        doctor.is_active = True
        doctor.save()
        return JsonResponse({'success': True, 'id': id, 'message': 'Doctor restored.'})
    return JsonResponse({'success': False}, status=400)
            

    
