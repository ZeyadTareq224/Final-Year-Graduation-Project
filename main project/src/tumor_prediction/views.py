from django.shortcuts import render
import requests
import json
import pandas as pd
from .forms import BCTestForm
from django.contrib.auth.decorators import login_required
from users.decorators import doctor_required
from clinics.models import Clinic
from django.views.decorators.http import require_http_methods

# Create your views here.

@require_http_methods(['GET', 'POST'])
@login_required(login_url="account_login")
@doctor_required
def BCTest(request):
    clinic = Clinic.objects.get(user=request.user)
    API_ENDPOINT = 'http://127.0.0.1:5000/predict'
    HEADERS = {'Content-type': 'application/json'}
    PREDICTION = None

    form = BCTestForm()
    if request.method == 'POST':
        form = BCTestForm(request.POST)
        if form.is_valid():
            radius_mean = form.cleaned_data['radius_mean']
            texture_mean = form.cleaned_data['texture_mean']
            perimeter_mean = form.cleaned_data['perimeter_mean']
            area_mean = form.cleaned_data['area_mean']
            smoothness_mean = form.cleaned_data['smoothness_mean']
            compactness_mean =form.cleaned_data['compactness_mean']
            concavity_mean = form.cleaned_data['concavity_mean']
            concave_points_mean = form.cleaned_data['concave_points_mean']
            symmetry_mean = form.cleaned_data['symmetry_mean']
            fractal_dimension_mean = form.cleaned_data['fractal_dimension_mean']
            obj ={
                "radius_mean": radius_mean,
                "texture_mean": texture_mean,
                "perimeter_mean": perimeter_mean,
                "area_mean": area_mean,
                "smoothness_mean": smoothness_mean,
                "compactness_mean": compactness_mean,
                "concavity_mean": concavity_mean,
                "concave_points_mean": concave_points_mean,
                "symmetry_mean": symmetry_mean,
                "fractal_dimension_mean": fractal_dimension_mean
            }
            
            response = requests.post(API_ENDPOINT, json=obj, headers=HEADERS)
            
            PREDICTION = response.json()['classification']
            if PREDICTION == 1:
                PREDICTION = 'Malignant '
            else:
                PREDICTION = 'Benign'
            form.instance.classification = PREDICTION
            form.instance.clinic = clinic
            form.save()


    context = {'form': form, 'prediction': PREDICTION}       
    return render(request, 'tumor_prediction/prediction.html', context)

