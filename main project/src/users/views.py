#DJANGO IMPORTS

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from allauth.account.views import SignupView, LoginView

#LOCAL IMPORTS
from .forms import DoctorSignUpForm, NormalUserSignUpForm
from .decorators import doctor_required, normal_user_required


def home_page(request):
    return render(request, 'users/index.html')

##########  SIGN UP VIEWS   ##########

def doctor_signup(request):
    form = DoctorSignUpForm()
    if request.method == "POST":
        form = DoctorSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('account_login')
    context = {'form': form}        
    return render(request, 'users/registration/signup_form.html', context)



def normal_user_signup(request):
    form = DoctorSignUpForm()
    if request.method == "POST":
        form = NormalUserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('account_login')
    context = {'form': form}        
    return render(request, 'users/registration/signup_form.html', context)

##########  END SIGN UP VIEWS   ##########


@login_required(login_url='account_login')
@doctor_required
def dochome(request):
    return HttpResponse("<h1>doc home</h1>")



@login_required(login_url='account_login')
@normal_user_required
def userhome(request):
    return HttpResponse("<h1>users home</h1>")

##########  REQUEST ERORR HANDLERS  ##########
def unauthorized(request):
    return render(request, 'users/request_errors/request_unauthorized.html', status=401)

##########  END REQUEST ERORR HANDLERS  ##########
