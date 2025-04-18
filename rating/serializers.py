from rest_framework import serializers
from .models import DoctorReview

class DoctorReviewSerializer(serializers.ModelSerializer):
    patient_username = serializers.CharField(source='patient.username', read_only=True)
    doctor_name = serializers.CharField(source='doctor.username', read_only=True)
    patient_picture = serializers.ImageField(source='patient.profile_picture', read_only=True)
    doctor_picture = serializers.CharField(source='doctor.username', read_only=True)
    first_name = serializers.CharField(source='patient.first_name', read_only=True)
    last_name = serializers.CharField(source='patient.last_name', read_only=True)
    class Meta:
        model = DoctorReview
        fields = ['id', 'patient_username','patient_picture','first_name','last_name', 'doctor', 'doctor_picture','doctor_name', 'rating', 'comment', 'created_at']
        ref_name = 'RatingDoctorReviewSerializer'

    def create(self, validated_data):
        validated_data['patient'] = self.context['request'].user
        return super().create(validated_data)
