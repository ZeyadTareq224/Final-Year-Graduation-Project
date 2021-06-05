from django.db import models
from django.contrib.auth import get_user_model
from clinics.models import Clinic
# Create your models here.
User = get_user_model()

class BCTest(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, null=True)
    radius_mean = models.CharField(max_length=256)
    texture_mean = models.CharField(max_length=256)
    perimeter_mean = models.CharField(max_length=256)
    area_mean = models.CharField(max_length=256)
    smoothness_mean = models.CharField(max_length=256)
    compactness_mean = models.CharField(max_length=256)
    concavity_mean = models.CharField(max_length=256)
    concave_points_mean = models.CharField(max_length=256)
    symmetry_mean = models.CharField(max_length=256)
    fractal_dimension_mean = models.CharField(max_length=256)
    classification = models.CharField(max_length=256, blank=True, null=True)
    patient_name = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return f"{self.clinic}_test id:{self.id}"


class BCTestFriendly(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, null=True)
    Clump_Thickness = models.CharField(max_length=256)
    Uniformity_of_Cell_Size = models.CharField(max_length=256)
    Uniformity_of_Cell_Shape = models.CharField(max_length=256)
    Marginal_Adhesion = models.CharField(max_length=256)
    Single_Epithelial_Cell_Size = models.CharField(max_length=256)
    Bare_Nuclei = models.CharField(max_length=256)
    Bland_Chromatin = models.CharField(max_length=256)
    Normal_Nucleoli = models.CharField(max_length=256)
    Mitoses = models.CharField(max_length=256)
    classification = models.CharField(max_length=256, blank=True, null=True)
    patient_name = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return f"{self.clinic}_test id:{self.id}"        