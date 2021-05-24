from django.urls import path
from . import views

urlpatterns = [
    path('', views.clinics, name="clinics"),
    path('create/', views.create_clinic, name="create_clinic"),
    path('<int:clinic_id>/', views.clinic_details, name="clinic_details"),
    path('update/<int:clinic_id>/', views.update_clinic, name="update_clinic"),
    path('add-clinic-review/<int:clinic_id>', views.add_clinic_review, name="add_clinic_review"),

    path('search/', views.search, name="clinics_search"),


    path('appointment/<int:clinic_id>', views.create_appointment, name="create_appointment"),
    path('manage-appointments/', views.manage_appointments, name="manage_appointments"),
    path('delete-appointment/<int:appointment_id>', views.delete_appointment, name="delete_appointment"),


    path('prescription/<int:patient_id>/<int:appointment_id>', views.add_prescription, name="add_prescription"),
    path('view-prescription/<int:appointment_id>', views.view_prescription, name="view_prescription"),

    path('appointment/<int:appointment_id>/reschedule/', views.reschedule_appointment, name="reschedule_appointment"),
    path('appointment/<int:appointment_id>/close/', views.close_appointment, name="close_appointment"),


    path('medical_history/', views.medical_history, name="medical_history"),
    


    path('bctest/history/<int:clinic_id>', views.BCT_history, name="BCT_history"),
    path('drugs-guide/', views.drugs_guide, name="drug_guide"),
]