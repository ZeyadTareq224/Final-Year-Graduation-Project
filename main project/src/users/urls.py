from django.urls import path, include
from . import views

urlpatterns = [
    path('accounts/signup/', views.normal_user_signup, name='normal_user_signup'),
    path('accounts/signup/doctor/', views.doctor_signup, name='doctor_signup'),

    path('accounts/', include('allauth.urls')),



    path('', views.home_page, name="home"),
    path('doc/', views.doc_home, name="dochome"),
    path('usr/', views.user_home, name="usrhome"),
    path('admin-dashboard/', views.admin_home, name="adminhome"),
    path('UA/', views.unauthorized, name="unauthorized")
]
