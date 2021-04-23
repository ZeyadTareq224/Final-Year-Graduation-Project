from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('Ai-Advice/', include('tumor_prediction.urls')),
    path('questions/', include('questions.urls')),
    path('clinics/', include('clinics.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from schema_graph.views import Schema
urlpatterns += [
    # On Django 2+:
    path("schema/", Schema.as_view()),
]