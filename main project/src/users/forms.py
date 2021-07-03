from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.contrib.auth import get_user_model
from .models import Profile, User, ApprovedDoctors

class DoctorSignUpForm(UserCreationForm):

    syndicate_id = forms.IntegerField()

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username', 'email', 'syndicate_id', 'password1', 'password2']

    def clean_syndicate_id(self):
        syndicate_id = self.cleaned_data.get('syndicate_id')
        print('syndicate_id: ', syndicate_id)
        if not ApprovedDoctors.objects.filter(syndicate_id=syndicate_id).exists():
            raise forms.ValidationError('Something wrong happened, check your sydicate id again')
        return syndicate_id

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