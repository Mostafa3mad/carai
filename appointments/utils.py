from datetime import datetime, timedelta
from .models import Appointment, DoctorAvailability, Weekday


def get_weekday_from_date(date_obj):
    """
    استخرج اسم اليوم من التاريخ (مثلاً: 'Monday')
    """
    return date_obj.strftime("%A")


def generate_time_slots(start_time, end_time, step_minutes=60):
    """
    إنشاء قائمة من الساعات المتاحة من وقت البدء حتى وقت الانتهاء.
    """
    current = datetime.combine(datetime.today(), start_time)
    end = datetime.combine(datetime.today(), end_time)
    slots = []
    while current < end:
        slots.append(current.time())
        current += timedelta(minutes=step_minutes)
    return slots


def is_doctor_available(doctor, weekday, appointment_time):
    """
    تحقق ما إذا كان الطبيب متاحًا في يوم ووقت معينين
    """
    return DoctorAvailability.objects.filter(
        doctor=doctor,
        days_of_week=weekday,
        available_from__lte=appointment_time,
        available_to__gt=appointment_time
    ).exists()


def get_doctor_availability_data(doctor):
    """
    إرجاع جدول التوافر للطبيب مع المواعيد المحجوزة
    """
    doctor_availability = DoctorAvailability.objects.filter(doctor=doctor)
    availability_data = []

    for availability in doctor_availability:
        for day in availability.days_of_week.all():
            start_time = availability.available_from
            end_time = availability.available_to

            slots = generate_time_slots(start_time, end_time)
            slot_strings = [slot.strftime("%H:%M") for slot in slots]

            appointments = [
                a for a in Appointment.objects.filter(
                    doctor=doctor,
                    status__in=["completed"]
                )
                if a.appointment_date.strftime("%A") == day.name
            ]

            booked_times = {a.appointment_time.strftime("%H:%M") for a in appointments}

            free_slots = [t for t in slot_strings if t not in booked_times]
            booked_slots = [
                {
                    "time": a.appointment_time.strftime("%H:%M"),
                    "date": a.appointment_date.strftime("%Y-%m-%d")
                }
                for a in appointments
            ]
            availability_data.append({
                "day": day.name,
                "available_from": start_time.strftime("%H:%M"),
                "available_to": end_time.strftime("%H:%M"),
                "free_slots": free_slots,
                "booked_slots": booked_slots,
            })

    return availability_data
