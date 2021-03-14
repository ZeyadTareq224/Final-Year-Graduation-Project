from django.forms import ModelForm
from .models import BCTest


class BCTestForm(ModelForm):
    class Meta:
        model = BCTest
        fields = [
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