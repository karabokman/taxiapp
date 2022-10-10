from django.contrib import admin
from .models import Taxi,Driver,Destination

# Register your models here.
admin.site.register(Taxi)
admin.site.register(Driver)
admin.site.register(Destination)
