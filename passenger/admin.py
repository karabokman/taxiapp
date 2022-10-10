from django.contrib import admin
from .models import Passenger,Booking,Ride,Hiring

# Register your models here.
admin.site.register(Passenger)
admin.site.register(Ride)
admin.site.register(Booking)
admin.site.register(Hiring)
