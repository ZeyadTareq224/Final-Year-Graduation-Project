from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib import messages
from .models import Clinic, ClinicReview, Appointment, Prescription
from .forms import ClinicForm, ClinicReviewForm, AppointmentForm, PrescriptionForm
from .helpers import get_rating_percentage
from django.db.models import Q
import datetime
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from tumor_prediction.models import BCTest, BCTestFriendly
from .drugs_scrapper import drugs1, drugs2, drugs3 
from django.contrib.auth.decorators import login_required
from users.decorators import doctor_required, normal_user_required
from django.views.decorators.http import require_http_methods
# Create your views here.

@require_http_methods(['GET'])
@login_required(login_url="account_login")
def clinics(request):
    clinics = Clinic.objects.all()
    context = {'clinics': clinics}
    return render(request, 'clinics/index.html', context)
    
@require_http_methods(['GET', 'POST'])
@login_required(login_url="account_login")
@doctor_required   
def create_clinic(request):
    user_clinic = Clinic.objects.filter(user=request.user)
    if not user_clinic:
        form = ClinicForm()
        if request.method == "POST":
            form = ClinicForm(request.POST)
            if form.is_valid():
                form.instance.user = request.user
                form.save()
                messages.success(request, "Your Clinic Created Successfully.")
                return redirect("clinics")
        context = {'form': form, 'user_clinic':user_clinic}
        return render(request, 'clinics/clinic_form.html', context)
    return render(request, 'clinics/request_errors/request_unauthorized.html')


@require_http_methods(['GET'])
@login_required(login_url="account_login")
def clinic_details(request, clinic_id):
    clinic = get_object_or_404(Clinic, id=clinic_id)    
    patient_appointment_count = Appointment.objects.filter(clinic=clinic, patient=request.user).count()
    reviews = ClinicReview.objects.filter(clinic=clinic).order_by('-id')
    rating_percentage = get_rating_percentage(reviews)
    form = ClinicReviewForm()
        
    context = {
        'clinic': clinic,
        'reviews': reviews,
        'rating_percentage': rating_percentage,
        'form': form,
        'patient_appointment_count': patient_appointment_count
        }
    return render(request, 'clinics/clinic_details.html', context)


@require_http_methods(['POST'])
@login_required(login_url="account_login")
def add_clinic_review(request, clinic_id):
    clinic = get_object_or_404(Clinic, id=clinic_id)    
    if request.method == "POST":
        form = ClinicReviewForm(request.POST)
        form.instance.clinic = clinic
        form.instance.patient = request.user
        form.save()
        messages.success(request, "Review Added Successfully.")
        return redirect("clinic_details", clinic_id)


@require_http_methods(['GET', 'POST', 'PUT'])
@login_required(login_url="account_login")
@doctor_required
def update_clinic(request, clinic_id):
    clinic = get_object_or_404(Clinic, id=clinic_id)
    if request.user != clinic.user:
        return render(request, 'clinics/request_errors/request_unauthorized.html', status=401)
    form = ClinicForm(instance=clinic)
    if request.method=="POST":
        form = ClinicForm(request.POST, instance=clinic)
        if form.is_valid():
            form.save()
            messages.success(request, "Your clinic's information successfully updated.")
            return redirect("clinic_details", clinic_id)
    context = {'form': form}
    return render(request, 'clinics/clinic_form.html', context)


@require_http_methods(['GET'])
@login_required(login_url="account_login")
def search(request):
    if request.method == "GET":
        query = request.GET.get('search_query', None)
        if query:
            clinics = Clinic.objects.filter(Q(title__icontains=query) | Q(city__icontains=query))
            context = {'clinics': clinics}
            return render(request, 'clinics/clinics_search.html', context)
        return render(request, 'clinics/clinics_search.html')


@require_http_methods(['GET', 'POST'])
@normal_user_required
@login_required(login_url="account_login")
def create_appointment(request, clinic_id): 
    clinic = Clinic.objects.get(id=clinic_id)
    user_appointments = Appointment.objects.filter(Q(patient=request.user), Q(clinic=clinic), ~Q(status="Closed"))
    
    if user_appointments.count() > 0:
        return render(request, 'clinics/request_errors/request_unauthorized.html', status=401)
    if request.method == "POST":
        new_appointment = Appointment(patient=request.user, clinic=clinic)
        new_appointment.save()
        send_mail("New Appointment", f"a new appointment got requested from {new_appointment.patient} at {new_appointment.created_at}. check your appointment mangagement page on BCCP.", 'ex.stunex@gmail.com', [clinic.user.email])
        messages.success(request, "Your Have reserved an appointment. wait for a confirmation email with the appointment date and time.")
        return redirect("clinic_details", clinic_id)
    return redirect("clinic_details", clinic_id)



@require_http_methods(['GET', 'POST'])
@login_required(login_url="account_login")
@doctor_required
def reschedule_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    form = AppointmentForm(instance=appointment)
    if request.method == "POST":
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            appointment.status = "Accepted"
            appointment.save()
            form.save()
            send_mail("Appointment rescheduled", f"Your appointment reschedule to {form.cleaned_data['date']} at {form.cleaned_data['time']}. check your appointment mangagement page on BCCP.", 'ex.stunex@gmail.com', [appointment.patient.email])
            messages.success(request, "Appointment rescheduled successfully.")
            return redirect("manage_appointments")
    context = {'form': form}
    return render(request, 'clinics/appointment_form.html', context)


@require_http_methods(['POST', 'DELETE'])
@login_required(login_url="account_login")
def delete_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    if request.method == "POST":
        appointment.delete()
        send_mail("Appointment rescheduled", f"Your appointment with {appointment.clinic} was rejected.", 'ex.stunex@gmail.com', [appointment.patient.email])
        return redirect('manage_appointments')


@require_http_methods(['GET'])
@login_required(login_url="account_login")
def manage_appointments(request):
    if request.user.is_normal_user:
        appointments = Appointment.objects.filter(Q(patient=request.user), ~Q(status="Closed"))

    if request.user.is_doctor:
        clinic = Clinic.objects.filter(user=request.user)[0]
        if not Clinic.objects.filter(user=request.user).exists():
            return render(request, 'clinics/request_errors/create_clinic_first.html')
        appointments = Appointment.objects.filter(clinic=clinic)
        
    context = {'appointments': appointments}
    return render(request, 'clinics/manage_appointments.html', context)



@require_http_methods(['GET'])
@login_required(login_url="account_login")
@normal_user_required
def view_prescription(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    prescription = Prescription.objects.get(appointment=appointment)
    context = {'prescription': prescription}
    return render(request, 'clinics/prescription_details.html', context)


@require_http_methods(['GET', 'POST'])
@login_required(login_url="account_login")
@doctor_required
def add_prescription(request, patient_id, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    if appointment.status == "Accepted":
        form = PrescriptionForm()
        patient = get_user_model().objects.get(id=patient_id)
        if request.method == "POST":
            form = PrescriptionForm(request.POST)
            if form.is_valid():
                form.instance.patient = patient
                form.instance.clinic = request.user.clinic
                form.instance.appointment = appointment
                form.save()
                messages.success(request, "Prescription added successfully.")
                send_mail("Doctor Prescription", "Your doctor finished your prescription check it out on BCCP.", 'ex.stunex@gmail.com', [patient.email])
                return redirect("manage_appointments")
        context = {'form': form}
        return render(request, 'clinics/prescription_form.html', context)
    
    messages.info(request, "You havent accepted the appointment yet. or it is closed already")
    return redirect("manage_appointments")


@require_http_methods(['GET'])
@login_required(login_url="account_login")
@doctor_required
def close_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = 'Closed'
    appointment.save()
    return redirect('manage_appointments')



@require_http_methods(['GET'])
@login_required(login_url="account_login")
@normal_user_required
def medical_history(request):
    prescriptions = Prescription.objects.filter(patient=request.user)
    context = {'prescriptions': prescriptions}
    return render(request, 'clinics/medical_history.html', context)



@require_http_methods(['GET'])
@login_required(login_url="account_login")
@doctor_required
def BCT_history(request, clinic_id):
    clinic = Clinic.objects.get(id=clinic_id)
    bctests = BCTest.objects.filter(clinic=clinic)
    context = {'bctests': bctests}
    return render(request, 'clinics/bct_history.html', context)

@require_http_methods(['GET'])
@login_required(login_url="account_login")
@doctor_required
def BCT_history_cell_analysis(request, clinic_id):
    clinic = Clinic.objects.get(id=clinic_id)
    bctests_cell_analysis = BCTestFriendly.objects.filter(clinic=clinic)
    context = {'bctests': bctests_cell_analysis}
    return render(request, 'clinics/bct_history_cell_analysis.html', context)

@require_http_methods(['GET'])
@login_required(login_url="account_login")
def drugs_guide(request):
    context = {'drugs1':drugs1, 'drugs2':drugs2, 'drugs3': drugs3}
    return render(request, 'clinics/drugs_guide.html', context)