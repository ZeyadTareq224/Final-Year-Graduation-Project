from django.shortcuts import render
import requests
import json
import pandas as pd
from .forms import BCTestForm, FriendlyBCTestForm
from django.contrib.auth.decorators import login_required
from users.decorators import doctor_required
from clinics.models import Clinic
from django.views.decorators.http import require_http_methods

# Create your views here.
@require_http_methods(['GET'])
@login_required(login_url="account_login")
@doctor_required
def ai_advice(request):
    
    return render(request, 'tumor_prediction/ai_advice.html')


@require_http_methods(['GET', 'POST'])
@login_required(login_url="account_login")
@doctor_required
def BCTest(request):
    clinic = Clinic.objects.get(user=request.user)
    API_ENDPOINT = 'http://127.0.0.1:5000/predict1'
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

def Friendly_BCTest(request):
    clinic = Clinic.objects.get(user=request.user)
    API_ENDPOINT = 'http://127.0.0.1:5000/predict2'
    HEADERS = {'Content-type': 'application/json'}
    PREDICTION = None

    form = FriendlyBCTestForm()
    if request.method == 'POST':
        form = FriendlyBCTestForm(request.POST)
        if form.is_valid():
            Clump_Thickness = form.cleaned_data['Clump_Thickness']
            Uniformity_of_Cell_Size = form.cleaned_data['Uniformity_of_Cell_Size']
            Uniformity_of_Cell_Shape = form.cleaned_data['Uniformity_of_Cell_Shape']
            Marginal_Adhesion = form.cleaned_data['Marginal_Adhesion']
            Single_Epithelial_Cell_Size = form.cleaned_data['Single_Epithelial_Cell_Size']
            Bare_Nuclei =form.cleaned_data['Bare_Nuclei']
            Bland_Chromatin = form.cleaned_data['Bland_Chromatin']
            Normal_Nucleoli = form.cleaned_data['Normal_Nucleoli']
            Mitoses = form.cleaned_data['Mitoses']
            obj ={
                "Clump_Thickness": Clump_Thickness,
                "Uniformity_of_Cell_Size": Uniformity_of_Cell_Size,
                "Uniformity_of_Cell_Shape": Uniformity_of_Cell_Shape,
                "Marginal_Adhesion": Marginal_Adhesion,
                "Single_Epithelial_Cell_Size": Single_Epithelial_Cell_Size,
                "Bare_Nuclei": Bare_Nuclei,
                "Bland_Chromatin": Bland_Chromatin,
                "Normal_Nucleoli": Normal_Nucleoli,
                "Mitoses": Mitoses,
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
    return render(request, 'tumor_prediction/prediction2.html', context)