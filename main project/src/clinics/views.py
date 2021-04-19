from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib import messages
from .models import Clinic, ClinicReview, Appointment, Prescription, Payment
from .forms import ClinicForm, ClinicReviewForm, AppointmentForm, PrescriptionForm, PaymentForm
from .helpers import get_rating_percentage
from django.db.models import Q
import datetime
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from tumor_prediction.models import BCTest
from .drugs_scrapper import drugs1, drugs2, drugs3 
# Create your views here.

def clinics(request):
    clinics = Clinic.objects.all()
    print(clinics[0])
    context = {'clinics': clinics}
    return render(request, 'clinics/index.html', context)
    
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


def clinic_details(request, clinic_id):
    clinic = get_object_or_404(Clinic, id=clinic_id)

    reviews = ClinicReview.objects.filter(clinic=clinic)
    rating_percentage = get_rating_percentage(reviews)
    form = ClinicReviewForm()
    if request.user != clinic.user:
        if request.method == "POST":
            form = ClinicReviewForm(request.POST)
            form.instance.clinic = clinic
            form.instance.patient = request.user
            form.save()
            messages.success(request, "Review Added Successfully.")
            return redirect("clinic_details", clinic_id)
        
    context = {
        'clinic': clinic,
        'reviews': reviews,
        'rating_percentage': rating_percentage,
        'form': form,
        }
    return render(request, 'clinics/clinic_details.html', context)

def update_clinic(request, clinic_id):
    clinic = get_object_or_404(Clinic, id=clinic_id)

    form = ClinicForm(instance=clinic)
    if request.method=="POST":
        form = ClinicForm(request.POST, instance=clinic)
        if form.is_valid():
            form.save()
            messages.success(request, "Your clinic data information successfully.")
            return redirect("clinic_details", clinic_id)
    context = {'form': form}
    return render(request, 'clinics/clinic_form.html', context)


def search(request):
    if request.method == "GET":
        query = request.GET.get('search_query', None)
        if query:
            clinics = Clinic.objects.filter(Q(title__icontains=query) | Q(city__icontains=query))
            context = {'clinics': clinics}
            return render(request, 'clinics/clinics_search.html', context)
        return render(request, 'clinics/clinics_search.html')


def create_appointment(request, clinic_id):
    
    clinic = Clinic.objects.get(id=clinic_id)
    if request.method == "POST":
        new_appointment = Appointment(patient=request.user, clinic=clinic)
        new_appointment.save()
        send_mail("New Appointment", f"a new appointment got requested from {new_appointment.patient} at {new_appointment.created_at}. check your appointment mangagement page on BCCP.", 'ex.stunex@gmail.com', [clinic.user.email])
        messages.success(request, "Your Have reserved an appointment. wait for a confirmation email with the appointment date and time.")
        return redirect("clinic_details", clinic_id)
    context = {'form': form}
    return redirect("clinic_details", clinic_id)


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


def delete_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    if request.method == "POST":
        appointment.delete()
        send_mail("Appointment rescheduled", f"Your appointment with {appointment.clinic} was rejected.", 'ex.stunex@gmail.com', [appointment.patient.email])
        return redirect('manage_appointments')



def manage_appointments(request):
    if request.user.is_normal_user:
        appointments = Appointment.objects.filter(patient=request.user)  
    elif request.user.is_doctor:
        clinic = Clinic.objects.get(user=request.user)
        appointments = Appointment.objects.filter(clinic=clinic)
        
    context = {'appointments': appointments}
    return render(request, 'clinics/manage_appointments.html', context)



def add_prescription(request, patient_id, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    if (appointment.status == "Accepted"):
        form = PrescriptionForm()
        patient = get_user_model().objects.get(id=patient_id)
        if request.method == "POST":
            form = PrescriptionForm(request.POST)
            if form.is_valid():
                form.instance.patient = patient
                form.instance.clinic = request.user.clinic
                form.save()
                messages.success(request, "Prescription added successfully.")
                form.save()
                send_mail("Doctor Prescription", "Your doctor finished your subscription check it out on BCCP.", 'ex.stunex@gmail.com', [patient.email])
                return redirect("manage_appointments")
        context = {'form': form}
        return render(request, 'clinics/prescription_form.html', context)
    else:
        messages.info(request, "You havent accepted the appointment yet.")
        return redirect("manage_appointments")


def patients_history(request, clinic_id):
    clinic = Clinic.objects.get(id=clinic_id)
    prescriptions = clinic.prescription_set.all()
    
    context = {'prescriptions': prescriptions}
    return render(request, 'clinics/patients_history.html', context)


def medical_history(request):
    prescriptions = Prescription.objects.filter(patient=request.user)

    context = {'prescriptions': prescriptions}
    return render(request, 'clinics/medical_history.html', context)


def add_payment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    if not appointment.paied:
        form = PaymentForm()
        if request.method == "POST":
            form = PaymentForm(request.POST)
            if form.is_valid():
                form.instance.patient = appointment.patient
                form.instance.clinic = appointment.clinic
                form.save()
                appointment.paied = True
                appointment.save()
                messages.success(request, "payment created successfully.")
                return redirect("manage_appointments")
        context = {'form': form}
        return render(request, 'clinics/payment_form.html', context)
    else:
        messages.warning(request, "patient already paied for this.")
        return redirect("manage_appointments")

def clinic_payment_history(request, clinic_id):
    clinic = Clinic.objects.get(id=clinic_id)
    payments = Payment.objects.filter(clinic=clinic)

    context = {'payments': payments}
    return render(request, 'clinics/clinic_payment_history.html', context)


def patient_payment_history(request):
    patient = request.user

    payments = Payment.objects.filter(patient=patient)

    context = {'payments': payments}
    return render(request, 'clinics/patient_payment_history.html', context)


def BCT_history(request, clinic_id):
    clinic = Clinic.objects.get(id=clinic_id)
    bctests = BCTest.objects.filter(clinic=clinic)
    context = {'bctests': bctests}
    return render(request, 'clinics/bct_history.html', context)


def drugs_guide(request):
    
    
    context = {'drugs1':drugs1, 'drugs2':drugs2, 'drugs3': drugs3}
    return render(request, 'clinics/drugs_guide.html', context)