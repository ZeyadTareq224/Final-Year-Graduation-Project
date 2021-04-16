from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Clinic)
admin.site.register(ClinicReview)
admin.site.register(Appointment)
admin.site.register(Prescription)
admin.site.register(Payment)

