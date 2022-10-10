# Generated by Django 4.1 on 2022-09-06 07:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hiring',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passenger', models.CharField(max_length=255)),
                ('date', models.DateField(auto_now_add=True)),
                ('For', models.DateField()),
                ('no_days', models.IntegerField()),
                ('status', models.CharField(default='Unpaid', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ride_no', models.CharField(max_length=255, unique=True)),
                ('d_from', models.CharField(max_length=255)),
                ('d_to', models.CharField(max_length=255)),
                ('driver_no', models.CharField(max_length=255)),
                ('taxi', models.CharField(max_length=255)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='Available', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passenger_no', models.CharField(max_length=255, unique=True)),
                ('img', models.ImageField(default='placeholder.jpeg', upload_to='p_img')),
                ('p_contacts', models.CharField(max_length=255)),
                ('contact_person', models.CharField(max_length=255)),
                ('e_contacts', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passenger_no', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
                ('p_contacts', models.CharField(max_length=255)),
                ('contact_person', models.CharField(max_length=255)),
                ('e_contacts', models.CharField(max_length=255)),
                ('ride_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='passenger.ride')),
            ],
        ),
    ]
