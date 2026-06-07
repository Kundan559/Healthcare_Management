from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import PatientSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Patient
from .forms import PatientForm
from accounts.decorators import allowed_users
from django.contrib.auth.decorators import login_required
from appointments.models import Appointment
from datetime import date
from django.http import JsonResponse
from django.urls import reverse



# Add Patient
@login_required
@allowed_users(['ADMIN', 'RECEPTION'])
def add_patient(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm()
            
    return render(
        request,
        'patients/add_patient.html',
        {'form':form}
    )

# View Patient
@login_required
@allowed_users(['ADMIN', 'DOCTOR', 'RECEPTION'])
def patient_list(request):

    query = request.GET.get('q')
    gender = request.GET.get('gender')

    patients = Patient.objects.all()

    if query:
        patients = patients.filter(
            Q(name__icontains=query) | Q(phone__icontains=query)
        )

    if gender:
        patients = patients.filter(gender__iexact=gender)

    genders = Patient.objects.order_by('gender').values_list('gender', flat=True).distinct()

    # Pagination
    paginator = Paginator(patients, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'patients': page_obj,
        'genders': genders,
        'page_obj': page_obj,
    }

    return render(
        request,
        'patients/patient_list.html',
        context
    )
    
# Patient Detail
@login_required
@allowed_users(['ADMIN', 'DOCTOR', 'RECEPTION'])
def patient_detail(request, id):
    patient = get_object_or_404(Patient, id=id)
    appointments = Appointment.objects.filter(patient=patient)
    upcoming_appointments = appointments.filter(appointment_date__gte=date.today()).count()
    next_appointment = appointments.filter(appointment_date__gte=date.today()).order_by('appointment_date', 'appointment_time').first()

    return render(
        request,
        'patients/patient_detail.html',
        {
            'patient': patient,
            'appointment_count': appointments.count(),
            'upcoming_appointments': upcoming_appointments,
            'next_appointment': next_appointment,
            'recent_appointments': appointments.order_by('-appointment_date', '-appointment_time')[:3],
        }
    )

# Edit Patient
@login_required
@allowed_users(['ADMIN', 'RECEPTION'])
def edit_patient(request,id):
    patient = get_object_or_404(Patient,id=id)
    
    if request.method == 'POST':
        form = PatientForm(
            request.POST,
            instance=patient
        )
        
        if form.is_valid():
            form.save()
            return redirect('patient_list')
        
    else:
        form = PatientForm(instance= patient)
    
    return render(
        request,
        'patients/edit_patient.html',
        {'form':form}
    )
    
# Delete Patient
@login_required
@allowed_users(['ADMIN', 'RECEPTION'])
def delete_patient(request,id):
    patient = get_object_or_404(Patient, id=id)
    patient.is_active = False
    patient.save()
        
    return redirect('patient_list')


@login_required
@allowed_users(['ADMIN', 'RECEPTION'])
def delete_patient_ajax(request, id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        patient = get_object_or_404(Patient, id=id)
        patient.is_active = False
        patient.save()
        undo_url = reverse('restore_patient_ajax', args=[id])
        return JsonResponse({'success': True, 'id': id, 'undo_url': undo_url, 'message': 'Patient deleted.'})
    return JsonResponse({'success': False}, status=400)


@login_required
@allowed_users(['ADMIN', 'RECEPTION'])
def restore_patient_ajax(request, id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        patient = get_object_or_404(Patient.all_objects, id=id)
        patient.is_active = True
        patient.save()
        return JsonResponse({'success': True, 'id': id, 'message': 'Patient restored.'})
    return JsonResponse({'success': False}, status=400)
        
#----------------------------
# ------- Rest API's --------  
#----------------------------

#Get Patient API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def patient_list_api(request):
    
    patients = Patient.objects.all()
    
    serializer = PatientSerializer(
        patients,
        many=True
    )
    return Response(
        serializer.data
    )
    
#Add Patient API
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_patient_api(request):
    
    serializer = PatientSerializer(data=request.data)
    
    if serializer.is_valid():
        
        serializer.save()
        
        return Response(
            serializer.data,
            status=201
        )
        
    return Response(
        serializer.errors,
        status=400
    )

    
