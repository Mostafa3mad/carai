from django.urls import path
from .views import DiagnosisAPIView


app_name = "model_ai"

urlpatterns = [
    path('predict/', DiagnosisAPIView.as_view(), name='ai-diagnosis'),
]
