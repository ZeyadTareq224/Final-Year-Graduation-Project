from django.urls import path
from . import views

urlpatterns = [
    path('prediction-expert/', views.BCTest, name="BCTest"),
    path('ai_advice/', views.ai_advice, name="ai_advice"),
    path('prediction-friendly/', views.Friendly_BCTest, name="Friendly_BCTest"),

]
