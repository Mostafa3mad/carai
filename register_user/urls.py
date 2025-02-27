from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SpecializationViewSet,DoctorViewSet

app_name = "register_user"
router = DefaultRouter()
router.register(r'specializations', SpecializationViewSet, basename='specialization')
router.register(r'All_doctors', DoctorViewSet, basename='doctor')



urlpatterns = [
    path("api/auth/", include("rest_registration.api.urls")),
    path('', include(router.urls)),

]
