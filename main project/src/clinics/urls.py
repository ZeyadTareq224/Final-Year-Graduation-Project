from django.urls import path
from . import views

urlpatterns = [
    path('', views.clinics, name="clinics"),
    path('create/', views.create_clinic, name="create_clinic"),
    path('<int:clinic_id>/', views.clinic_details, name="clinic_details"),
    path('update/<int:clinic_id>/', views.update_clinic, name="update_clinic"),
    path('search/', views.search, name="clinics_search"),
    path('appointment/<int:clinic_id>', views.create_appointment, name="create_appointment"),
    path('manage-appointments/', views.manage_appointments, name="manage_appointments"),
    path('prescription/<int:patient_id>/<int:appointment_id>', views.add_prescription, name="add_prescription"),
    path('appointment/<int:appointment_id>/reschedule/', views.reschedule_appointment, name="reschedule_appointment"),
    path('patients/history/<int:clinic_id>', views.patients_history, name="patients_history"),
    path('medical_history/', views.medical_history, name="medical_history"),
    path('clinic_payment_history/<int:clinic_id>', views.clinic_payment_history, name="clinic_payment_history"),
    path('patient_payment_history/', views.patient_payment_history, name="patient_payment_history"),
    path('payment/<int:appointment_id>', views.add_payment, name="add_payment"),
    path('bctest/history/<int:clinic_id>', views.BCT_history, name="BCT_history"),
    path('drugs-guide/', views.drugs_guide, name="drugs_guide"),
]