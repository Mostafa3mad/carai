# Generated by Django 5.1.6 on 2025-02-25 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register_user', '0003_specialization_customuser_consultation_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
