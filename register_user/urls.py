from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SpecializationViewSet,DoctorViewSet,LogoutView,LoginView
from rest_registration.api.views import login,register,change_password,profile

app_name = "register_user"
router = DefaultRouter()
router.register(r'specializations', SpecializationViewSet, basename='specialization')
router.register(r'All_doctors', DoctorViewSet, basename='doctor')



urlpatterns = [
    # path("api/auth/", include("rest_registration.api.urls")),
    # path("api/login/", login, name="login"),
    path("api/login/", LoginView.as_view(), name="login"),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/register/', register, name='register'),
    path('api/register/', register, name='register'),
    path('api/change-password/', change_password, name='change-password'),
    path('api/profile/', profile, name='profile'),

    path('', include(router.urls)),

]
