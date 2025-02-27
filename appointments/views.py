from rest_framework import viewsets
from .models import Appointment
from .serializers import AppointmentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import DoctorAvailability
from .serializers import DoctorAvailabilitySerializer
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta,date


class AvailableAppointmentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, doctor_id, *args, **kwargs):
        doctor_availabilities = DoctorAvailability.objects.filter(doctor_id=doctor_id)

        if not doctor_availabilities:
            return Response({"message": "No available schedule found for this doctor."},
                            status=status.HTTP_404_NOT_FOUND)

        # تقسيم الساعات المتاحة للطبيب
        available_slots = []
        for availability in doctor_availabilities:
            for day in availability.days_of_week.all():
                start_time = availability.available_from
                end_time = availability.available_to

                # إضافة كل ساعة في اليوم كموعد
                while start_time < end_time:
                    available_slots.append({
                        "day": day.name,
                        "time": start_time.strftime("%H:%M"),
                        "is_booked": False  # هذا الحقل سنقوم بتحديثه لاحقًا بناءً على الحجز
                    })
                    start_time = (datetime.combine(date.today(), start_time) + timedelta(hours=1)).time()

        return Response({"available_slots": available_slots}, status=status.HTTP_200_OK)

class DoctorAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = DoctorAvailability.objects.all()
    serializer_class = DoctorAvailabilitySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # التأكد من أن المستخدم هو الطبيب


        if self.request.user.role != 'doctor':
            return Response({"detail": "Only doctors can set availability."}, status=status.HTTP_403_FORBIDDEN)

        # تحديد الطبيب تلقائيًا بناءً على المستخدم المسجل
        serializer.save(doctor=self.request.user)

    def list(self, request, *args, **kwargs):
        """إرجاع مواعيد الطبيب المسجل دخوله"""
        if self.request.user.role != 'doctor':  # التحقق من أن المستخدم هو الطبيب فقط
            return Response({"detail": "Only doctors can view availability."}, status=status.HTTP_403_FORBIDDEN)
        doctor_availabilities = DoctorAvailability.objects.filter(doctor=request.user)
        serializer = self.get_serializer(doctor_availabilities, many=True)
        return Response(serializer.data)


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def perform_create(self, serializer):
        # التأكد من أن المستخدم هو مريض (patient)
        if self.request.user.role != 'patient':
            return Response({"detail": "Only patients can book appointments."}, status=status.HTTP_403_FORBIDDEN)

        # تحديد المريض تلقائيًا من المستخدم المسجل
        patient = self.request.user  # المريض هو المستخدم الذي قام بتسجيل الدخول
        doctor = serializer.validated_data['doctor']  # الطبيب الذي يود المريض حجز موعد معه
        appointment_date = serializer.validated_data['appointment_date']  # الموعد الذي اختاره المريض

        # التحقق من أن الموعد ضمن مواعيد الطبيب المتاحة
        available_times = DoctorAvailability.objects.filter(doctor=doctor)
        valid_appointment = False
        for availability in available_times:
            if availability.available_from <= appointment_date.time() <= availability.available_to:
                valid_appointment = True
                break

        if not valid_appointment:
            return Response({"detail": "The selected appointment time is not available."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer.save(patient=patient, status='pending')
