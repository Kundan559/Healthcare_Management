from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Appointment
from .forms import AppointmentForm
from doctors.models import Doctor
from django.http import JsonResponse
from accounts.decorators import allowed_users

# Create your views here.
@login_required
@allowed_users(['ADMIN', 'DOCTOR', 'RECEPTION'])
def appointment_list(request):
    appointments = Appointment.objects.all()
    doctors = Doctor.objects.all()

    status = request.GET.get('status')
    patient = request.GET.get('patient')
    doctor_id = request.GET.get('doctor')
    department = request.GET.get('department')
    appointment_date = request.GET.get('date')

    if status:
        appointments = appointments.filter(status=status)

    if patient:
        appointments = appointments.filter(patient__name__icontains=patient)

    if doctor_id:
        appointments = appointments.filter(doctor_id=doctor_id)

    if department:
        appointments = appointments.filter(doctor__specialization__icontains=department)

    if appointment_date:
        appointments = appointments.filter(appointment_date=appointment_date)

    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(appointments.order_by('appointment_date', 'appointment_time'), 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'appointments': page_obj,
        'doctors': doctors,
        'page_obj': page_obj,
    }

    return render(
        request,
        'appointments/appointment_list.html',
        context
    )
    
# Appointment Detail
@login_required
@allowed_users(['ADMIN', 'DOCTOR', 'RECEPTION'])
def appointment_detail(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    return render(
        request,
        'appointments/appointment_detail.html',
        {'appointment': appointment}
    )

# Add Appointment
@login_required
@allowed_users(['ADMIN', 'RECEPTION'])
def add_appointment(request):
    doctors = Doctor.objects.all()
    
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
        
    else:
        form = AppointmentForm()
        
    return render(
        request,'appointments/add_appointment.html',
        {
            'form':form,
         'doctors':doctors
        }
    )
        
# Edit Appointment
@login_required
@allowed_users(['ADMIN', 'RECEPTION'])
def edit_appointment(request,id):
    appointment = get_object_or_404(Appointment,id=id)
    doctors = Doctor.objects.all()
    
    if request.method == "POST":
        form = AppointmentForm(
            request.POST,
            instance=appointment
        )
        
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
        
    else:
        form = AppointmentForm(
            instance=appointment
        )
        
    return render(
        request,'appointments/edit_appointment.html',
        {'form':form,
         'doctors':doctors,
         }
    )
        
# Delete Appointment
@login_required
@allowed_users(['ADMIN', 'RECEPTION'])
def delete_appointment(request,id):
    # Prefer POST for deletions — if GET, redirect to list
    if request.method == 'POST':
        appointment = get_object_or_404(Appointment,id=id)
        appointment.is_active = False
        appointment.save()
        messages.success(request, 'Appointment deleted.')
        return redirect(request.POST.get('next') or 'appointment_list')

    return redirect('appointment_list')


# Confirm Appointment
@login_required
@allowed_users(['ADMIN', 'DOCTOR', 'RECEPTION'])
def confirm_appointment(request, pk):
    # Accept POST to change state and return to `next` if provided
    if request.method == 'POST':
        appointment = get_object_or_404(Appointment, id=pk)
        appointment.status = 'CONFIRMED'
        appointment.save()
        messages.success(request, 'Appointment confirmed.')
        return redirect(request.POST.get('next') or 'appointment_list')
    return redirect('appointment_list')


@login_required
@allowed_users(['ADMIN', 'DOCTOR', 'RECEPTION'])
def confirm_appointment_ajax(request, pk):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        appointment = get_object_or_404(Appointment, id=pk)
        appointment.status = 'CONFIRMED'
        appointment.save()
        return JsonResponse({'success': True, 'status': appointment.status})
    return JsonResponse({'success': False}, status=400)


# Complete Appointment
@login_required
@allowed_users(['ADMIN', 'DOCTOR', 'RECEPTION'])
def complete_appointment(request, pk):
    if request.method == 'POST':
        appointment = get_object_or_404(Appointment, id=pk)
        appointment.status = 'COMPLETED'
        appointment.save()
        messages.success(request, 'Appointment marked as completed.')
        return redirect(request.POST.get('next') or 'appointment_list')
    return redirect('appointment_list')


@login_required
@allowed_users(['ADMIN', 'DOCTOR', 'RECEPTION'])
def complete_appointment_ajax(request, pk):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        appointment = get_object_or_404(Appointment, id=pk)
        appointment.status = 'COMPLETED'
        appointment.save()
        return JsonResponse({'success': True, 'status': appointment.status})
    return JsonResponse({'success': False}, status=400)


# Cancel Appointment
@login_required
@allowed_users(['ADMIN', 'DOCTOR', 'RECEPTION'])
def cancel_appointment(request, pk):
    if request.method == 'POST':
        appointment = get_object_or_404(Appointment, id=pk)
        appointment.status = 'CANCELLED'
        appointment.save()
        messages.success(request, 'Appointment cancelled.')
        return redirect(request.POST.get('next') or 'appointment_list')
    return redirect('appointment_list')


@login_required
@allowed_users(['ADMIN', 'DOCTOR', 'RECEPTION'])
def cancel_appointment_ajax(request, pk):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        appointment = get_object_or_404(Appointment, id=pk)
        appointment.status = 'CANCELLED'
        appointment.save()
        return JsonResponse({'success': True, 'status': appointment.status})
    return JsonResponse({'success': False}, status=400)


@login_required
@allowed_users(['ADMIN', 'RECEPTION'])
def delete_appointment_ajax(request, id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        appointment = get_object_or_404(Appointment, id=id)
        appointment.is_active = False
        appointment.save()
        from django.urls import reverse
        undo_url = reverse('restore_appointment_ajax', args=[id])
        return JsonResponse({'success': True, 'id': id, 'undo_url': undo_url, 'message': 'Appointment deleted.'})
    return JsonResponse({'success': False}, status=400)


@login_required
@allowed_users(['ADMIN', 'RECEPTION'])
def restore_appointment_ajax(request, id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        appointment = get_object_or_404(Appointment.all_objects, id=id)
        appointment.is_active = True
        appointment.save()
        return JsonResponse({'success': True, 'id': id, 'message': 'Appointment restored.'})
    return JsonResponse({'success': False}, status=400)
