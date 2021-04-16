from django.db import models
from django.contrib.auth import get_user_model
from clinics.models import Clinic
# Create your models here.
User = get_user_model()

class BCTest(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, on_delete=models.CASCADE)

    radius_mean = models.CharField(max_length=255)
    texture_mean = models.CharField(max_length=255)
    perimeter_mean = models.CharField(max_length=255)
    area_mean = models.CharField(max_length=255)
    smoothness_mean = models.CharField(max_length=255)
    compactness_mean = models.CharField(max_length=255)
    concavity_mean = models.CharField(max_length=255)
    concave_points_mean = models.CharField(max_length=255)
    symmetry_mean = models.CharField(max_length=255)
    fractal_dimension_mean = models.CharField(max_length=255)
    classification = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.doctor.username}_test"
    
        