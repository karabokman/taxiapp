from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Passenger(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    passenger_no = models.CharField(max_length=255, unique=True)
    img = models.ImageField(upload_to='p_img', default='placeholder.jpeg')
    p_contacts = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    e_contacts = models.CharField(max_length=255)

    def __str__(self):
        return self.passenger_no


class Ride(models.Model):
    ride_no = models.CharField(max_length=255, unique=True)
    d_from = models.CharField(max_length=255)
    d_to = models.CharField(max_length=255)
    driver_no = models.CharField(max_length=255)
    taxi = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, default="Available")

    def __str__(self):
        return self.ride_no


class Booking(models.Model):
    ride_no = models.ForeignKey(Ride, on_delete=models.CASCADE)
    passenger_no = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    p_contacts = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    e_contacts = models.CharField(max_length=255)

    def __str__(self):
        nam = self.ride_no.ride_no+ " "+self.passenger_no
        return nam


class Hiring(models.Model):
    reference = models.CharField(max_length=255, unique=True)
    passenger = models.ForeignKey(Passenger,null=True, on_delete=models.SET_NULL)
    date = models.DateField(auto_now_add=True)
    For = models.DateField()
    no_days = models.IntegerField()
    status = models.CharField(max_length=255, default="Unpaid")

    def __str__(self):
        return self.reference


