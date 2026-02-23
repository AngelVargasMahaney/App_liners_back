"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api.controllers import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   path("api/entities-by-campaign", EntityAPIViewCampain.as_view()),
   path("api/entities", EntityAPIView.as_view()),
    path("api/entities/<int:pk>", EntityAPIView.as_view()),

    path("api/activities", ActivityAPIView.as_view()),
    path("api/activities/<int:pk>", ActivityAPIView.as_view()),

    path("api/register-heads", RegisterHeadAPIView.as_view()),
    path("api/register-heads/<int:pk>", RegisterHeadAPIView.as_view()),

    path("api/ubications", UbicationAPIView.as_view()),
    path("api/ubications/<int:pk>", UbicationAPIView.as_view()),

    path("api/jobs", JobAPIView.as_view()),
    path("api/jobs/<int:pk>", JobAPIView.as_view()),
    
    path("api/equipments", EquipmentAPIView.as_view()),
    path("api/equipments/<int:pk>", EquipmentAPIView.as_view()),

    path("api/register-files", RegisterFilesAPIView.as_view()),
    path("api/register-files/<int:pk>", RegisterFilesAPIView.as_view()),

    path("api/register-details", RegisterDetailAPIView.as_view()),
    path("api/register-details/<int:pk>", RegisterDetailAPIView.as_view()),
    
    path("api/projects-available", ProjectsByEquipoAPIView.as_view()),
    path("api/pistolas-torque", PistolasTorqueAPIView.as_view()),
    path("api/pistolas-torque/<int:pk>", PistolasTorqueAPIView.as_view()),
    path("api/activities-by-project", ActivitiesByProjectAPIView.as_view()),
    path("api/register-heads-by-project-eq", RegisterHeadByProjectAPIView.as_view()),
    
    path("api/current-reg-detail", CurrentRegisterDetailAPIView.as_view()),

    path('api/admin/', admin.site.urls),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)