from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.contrib.auth import get_user_model
from .models import Profile
from .models import User

class DoctorSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']

    def save(self):
        user = super().save(commit=False)
        user.is_doctor = True
        user.save()
        return user

class NormalUserSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('A user has already registered using this email')
        return email
        
    def save(self):
        user = super().save(commit=False)
        user.is_normal_user = True
        user.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']