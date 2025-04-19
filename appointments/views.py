from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from datetime import datetime, timedelta, date
from django.db import transaction
from collections import defaultdict
from .permissions import IsPatient
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Appointment, DoctorAvailability, CustomUser, Weekday
from .serializers import AppointmentSerializer, DoctorAvailabilitySerializer
from .utils import (
    get_weekday_from_date,
    is_doctor_available,
    get_doctor_availability_data,
    generate_time_slots
)




class DoctorAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = DoctorAvailability.objects.all()
    serializer_class = DoctorAvailabilitySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != 'doctor':
            return Response({"detail": "Only doctors can set availability."}, status=status.HTTP_403_FORBIDDEN)
        serializer.save(doctor=self.request.user)

    def list(self, request, *args, **kwargs):
        if self.request.user.role != 'doctor':
            return Response({"detail": "Only doctors can view availability."}, status=status.HTTP_403_FORBIDDEN)

        doctor_availabilities = DoctorAvailability.objects.filter(doctor=request.user)
        serializer = self.get_serializer(doctor_availabilities, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        availability = self.get_object()
        if availability.doctor != request.user:
            return Response({"detail": "You cannot modify another doctor's availability."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        availability = self.get_object()
        if availability.doctor != request.user:
            return Response({"detail": "You cannot modify another doctor's availability."}, status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if request.user.role != 'doctor':
            return Response({"detail": "Only doctors can view their availability."}, status=status.HTTP_403_FORBIDDEN)

        availability = self.get_object()
        if availability.doctor != request.user:
            return Response({"detail": "You cannot view availability for another doctor."}, status=status.HTTP_403_FORBIDDEN)

        return super().retrieve(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def doctor_schedule(self, request):
        doctor = request.user
        if doctor.role != 'doctor':
            return Response({"error": "المستخدم ليس طبيبًا"}, status=400)

        doctor_availabilities = DoctorAvailability.objects.filter(doctor=doctor)
        schedule_data = []
        for availability in doctor_availabilities:
            available_times = []
            for day in availability.days_of_week.all():
                available_times.append({
                    "day": day.name,
                    "available_from": availability.available_from,
                    "available_to": availability.available_to,
                })
            schedule_data.append({"doctor": doctor.username, "schedule": available_times})

        return Response({"doctor_schedule": schedule_data})

    @action(detail=False, methods=['get'], url_path='appointments_by_day')
    def appointments_by_day(self, request):
        doctor = request.user
        if doctor.role != 'doctor':
            return Response({"error": "المستخدم ليس طبيبًا"}, status=403)

        appointments = Appointment.objects.filter(
            doctor=doctor
        ).order_by('appointment_date', 'appointment_time')

        serializer = AppointmentSerializer(appointments, many=True, context={'request': request})
        grouped = defaultdict(list)

        for appt in serializer.data:
            date = appt.get("appointment_date")
            grouped[date].append(appt)

        return Response(grouped)





class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, IsPatient]


    def get_queryset(self):
        user = self.request.user
        return Appointment.objects.filter(patient=user).order_by('-appointment_date', '-appointment_time')

    @action(detail=True, methods=['post'], url_path='simulate_payment')
    def simulate_payment(self, request, pk=None):
        appointment = self.get_object()

        if appointment.patient != request.user:
            return Response({"error": "لا يمكنك الدفع لهذا الموعد"}, status=403)

        if appointment.payment_status == 'paid':
            return Response({"message": "تم الدفع مسبقًا"}, status=400)

        # 🛑 تحقق من أن الموعد ما اتأكدش لمريض آخر في نفس الوقت
        conflict = Appointment.objects.filter(
            doctor=appointment.doctor,
            appointment_date=appointment.appointment_date,
            appointment_time=appointment.appointment_time,
            payment_status='paid',
        ).exclude(id=appointment.id)

        if conflict.exists():
            return Response({
                "error": "عذرًا، تم تأكيد هذا الموعد لمريض آخر.",
                "suggestion": "يرجى اختيار موعد آخر."
            }, status=400)

        # ✅ كل شيء تمام → نؤكد الحجز
        appointment.payment_status = 'paid'
        appointment.status = 'confirmed'
        appointment.save()


        # ✅ أضف 5 نقاط بونص للمريض
        patient = appointment.patient
        patient.bonus_points += 5
        patient.save()

        return Response({
            "message": "✅ تم الدفع بنجاح وتم تأكيد الموعد.",
            "new_bonus": patient.bonus_points
        }),



    @action(detail=False, methods=['get', 'post'])
    def doctor_availability(self, request):


        doctor_id = request.query_params.get('doctor_id')

        if not doctor_id:
            return Response({"error": "يجب إرسال doctor_id في URL"}, status=400)

        try:
            doctor = CustomUser.objects.get(id=doctor_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "الطبيب غير موجود"}, status=404)

        if doctor.role != 'doctor':
            return Response({"error": "المستخدم ليس طبيبًا"}, status=400)

        if request.method == 'GET':
            availability_data = get_doctor_availability_data(doctor)
            return Response({"doctor_availability": availability_data})


        elif request.method == 'POST':

            date_str = request.data.get('appointment_date')

            time_str = request.data.get('appointment_time')

            patient = request.user

            if not date_str or not time_str:
                return Response({"error": "يجب إرسال appointment_date و appointment_time"}, status=400)

            try:

                appointment_date = datetime.strptime(date_str, "%Y-%m-%d").date()

                appointment_time = datetime.strptime(time_str, "%H:%M").time()

            except ValueError:

                return Response({"error": "تنسيق التاريخ أو الوقت غير صالح"}, status=400)

            if appointment_date < date.today():
                return Response({"error": "لا يمكن الحجز في تاريخ ماضي"}, status=400)

            weekday_name = get_weekday_from_date(appointment_date)

            try:

                weekday = Weekday.objects.get(name=weekday_name)

            except Weekday.DoesNotExist:

                return Response({"error": "اليوم غير موجود"}, status=400)

            if not is_doctor_available(doctor, weekday, appointment_time):
                return Response({"error": "الطبيب غير متاح في هذا الموعد"}, status=400)

            with transaction.atomic():

                conflict = Appointment.objects.filter(

                    doctor=doctor,

                    appointment_date=appointment_date,

                    appointment_time=appointment_time,

                    status__in=["pending", "confirmed", "completed"]

                )

                if conflict.exists():
                    return Response({"error": "هذا الموعد محجوز بالفعل"}, status=400)

                appointment = Appointment.objects.create(

                    patient=patient,

                    doctor=doctor,

                    appointment_date=appointment_date,

                    appointment_time=appointment_time,

                    status='pending',

                    payment_status='pending'

                )

                availability_data = get_doctor_availability_data(doctor)

                return Response({

                    "message": "تم حجز المعاد بنجاح يرجى اكمال الدفع لتاكيد الحجز .",

                    "appointment_id": appointment.id,

                }, status=201)