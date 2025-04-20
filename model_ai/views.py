from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import joblib
from .utils import preprocess_text
import sys


sys.modules['__main__'].preprocess_text = preprocess_text

# تحميل الموديلات مرة واحدة
models = joblib.load("model_ai/chatbot_models.pkl")
medical_classifier = models["medical_classifier"]
disease_classifier = models["disease_and_specialization_classifier"]
label_encoder = models["label_encoder"]

class DiagnosisAPIView(APIView):
    def post(self, request):
        symptom = request.data.get("symptom", "")
        processed = preprocess_text(symptom)

        if not processed:
            return Response({"error": "Empty or invalid input."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            is_medical = medical_classifier.predict([processed])[0]
            if is_medical == 1:
                label_encoded = disease_classifier.predict([processed])[0]
                label = label_encoder.inverse_transform([label_encoded])[0]

                return Response({
                    "prediction": label,
                    "note": "🤖 I'm just an AI assistant providing an initial assessment.\nFor your safety, please consult a doctor for an accurate diagnosis and proper medical advice. 🏥💙"
                })
            else:
                return Response({"error": "please enter a text related to the medical field so I can assist you 🧠"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
