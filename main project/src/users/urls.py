from django.urls import path, include
from . import views

urlpatterns = [
    path('accounts/signup/', views.normal_user_signup, name='normal_user_signup'),
    path('accounts/signup/doctor/', views.doctor_signup, name='doctor_signup'),

    path('accounts/', include('allauth.urls')),
    path('profile/', views.user_profile, name="user_profile"),


    path('', views.home_page, name="home"),
    
    path('UA/', views.unauthorized, name="unauthorized")
]
