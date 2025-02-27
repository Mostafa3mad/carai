from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=(('male', 'Male'), ('female', 'Female')), blank=True, null=True)
    age = models.IntegerField(null=True, blank=True)

    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=15,choices=ROLE_CHOICES,default='patient',)
    specialization = models.ForeignKey('Specialization', on_delete=models.SET_NULL, null=True, blank=True)
    consultation_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # سعر الكشف
    location = models.CharField(max_length=255, null=True, blank=True)
    is_approved = models.BooleanField(default=True)




    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


#Specialization
class Specialization(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

