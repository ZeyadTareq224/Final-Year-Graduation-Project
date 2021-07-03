#DJANGO IMPORTS

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from allauth.account.views import SignupView, LoginView
from django.views.decorators.http import require_http_methods

#LOCAL IMPORTS
from .forms import DoctorSignUpForm, NormalUserSignUpForm, ProfileForm
from .decorators import doctor_required, normal_user_required
from .models import Profile

@require_http_methods(['GET'])
def home_page(request):
    return render(request, 'users/index.html')

##########  SIGN UP VIEWS   ##########

@require_http_methods(['GET', 'POST'])
def doctor_signup(request):
    form = DoctorSignUpForm()
    if request.method == "POST":
        form = DoctorSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('account_login')
    context = {'form': form}        
    return render(request, 'users/registration/signup_form.html', context)


@require_http_methods(['GET', 'POST'])
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

########## Profile View ########

@require_http_methods(['GET', 'POST'])
def user_profile(request):
    user_profile = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=user_profile)
    if request.method == "POST":
        print("accessed")
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Profile Data Updated successfully")
            return redirect('home')
    context = {'form': form}
    return render(request, 'users/user_profile.html', context)

########## END Profile View ######## 


##########  REQUEST ERORR HANDLERS  ##########


@require_http_methods(['GET'])
def unauthorized(request):
    return render(request, 'users/request_errors/request_unauthorized.html', status=401)


##########  END REQUEST ERORR HANDLERS  ##########
