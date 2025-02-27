from rest_framework import serializers
from .models import Appointment,DoctorAvailability,Weekday

class AppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.CharField(source='patient.username', read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'appointment_date', 'status']

class WeekdaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Weekday
        fields = ['name']


class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    doctor = serializers.CharField(source='doctor.username', read_only=True)
    days_of_week = serializers.ListField(
        child=serializers.CharField(max_length=20),
        write_only=True
    )

    class Meta:
        model = DoctorAvailability
        fields = ['id', 'doctor', 'available_from', 'available_to', 'days_of_week']

    def create(self, validated_data):
        days_of_week = validated_data.pop('days_of_week', [])
        instance = super().create(validated_data)

        # إضافة الأيام المتاحة للمواعيد
        instance.days_of_week.set(
            Weekday.objects.filter(name__in=days_of_week)
        )

        return instance

    def to_representation(self, instance):
        """عرض أسماء الأيام في استجابة الـ API"""
        representation = super().to_representation(instance)
        # تحويل الـ ManyToManyField إلى أسماء الأيام مباشرة
        representation['days_of_week'] = [day.name for day in instance.days_of_week.all()]
        return representation