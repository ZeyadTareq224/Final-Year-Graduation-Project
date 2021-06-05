from django.forms import ModelForm
from .models import BCTest, BCTestFriendly


class BCTestForm(ModelForm):
    class Meta:
        model = BCTest
        fields = [

            'patient_name',
            'radius_mean',
            'texture_mean',
            'perimeter_mean',
            'area_mean',
            'smoothness_mean',
            'compactness_mean',
            'concavity_mean',
            'concave_points_mean',
            'symmetry_mean',
            'fractal_dimension_mean',
        ]

class FriendlyBCTestForm(ModelForm):
    class Meta:
        model = BCTestFriendly
        fields = [
            'patient_name',
            'Clump_Thickness',
            'Uniformity_of_Cell_Size',
            'Uniformity_of_Cell_Shape',
            'Marginal_Adhesion',
            'Single_Epithelial_Cell_Size',
            'Bare_Nuclei',
            'Bland_Chromatin',
            'Normal_Nucleoli',
            'Mitoses'
        ]        