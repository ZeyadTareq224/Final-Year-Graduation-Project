from django import forms
from .models import *


class ClinicForm(forms.ModelForm):
    class Meta:
        model = Clinic
        fields = ['title', 'city', 'address', 'description', 'working_from', 'working_till']

        widgets = {
            'working_from': forms.TimeInput(attrs={'type': 'time'}),
            'working_till': forms.TimeInput(attrs={'type': 'time'}),
        }


class ClinicReviewForm(forms.ModelForm):
    class Meta:
        model = ClinicReview
        fields = ['comment_review', 'rating']


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'time']
        widgets = {
            'date': forms.TimeInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['symptoms', 'prescription']
