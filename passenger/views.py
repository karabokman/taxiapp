from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Passenger,Hiring,Ride,Booking
from driver.models import Taxi,Driver
from django.core.paginator import Paginator
from owner.models import Transactions
from random import randrange
from django.contrib.auth.decorators import user_passes_test,login_required
from django.utils.decorators import method_decorator

decoraters = [login_required(login_url='/auth/login'),user_passes_test(lambda u: u.groups.filter(name='passenger').exists())]

# Create your views here.
@method_decorator(decoraters,name='dispatch')
class IndexView(View):
    def get(self, request):
        user = request.user
        passenger = Passenger.objects.get(user=request.user)
        routes = Ride.objects.filter(status="Available")[:5]

        context = {
            'user': user,
            'passenger': passenger,
            'routes': routes,
        }
        return render(request, 'passenger/index.html', context)

@method_decorator(decoraters,name='dispatch')
class ProfileView(View):

    def get(self, request):
        user = request.user
        passenger = Passenger.objects.get(user=request.user)

        context = {
            'user': user,
            'passenger': passenger,
        }
        return render(request, 'passenger/profile.html', context)


    def post(self, request):
        user = User.objects.get(username=request.user.username)
        passenger = Passenger.objects.get(user=request.user)

        name = request.POST['name']
        surname = request.POST['surname']
        email = request.POST['email']
        p_no = request.POST['pcontact']
        contact_p = request.POST['contact-person']
        e_no = request.POST['econtact']

        user.first_name = name
        user.last_name = surname
        user.email = email
        user.save()

        if request.FILES.get('image') == None:

            img = passenger.img

            passenger.img = img
            passenger.p_contacts = p_no
            passenger.contact_person = contact_p
            passenger.e_contacts = e_no
            passenger.save()

        if request.FILES.get('image') != None:
            img = request.FILES.get('image')

            passenger.img = img
            passenger.p_contacts = p_no
            passenger.contact_person = contact_p
            passenger.e_contacts = e_no
            passenger.save()

        messages.success(request, 'Information updated successfully.')
        return redirect('profile')

@method_decorator(decoraters,name='dispatch')
class DestinationView(View):

    def get(self, request):
        user = request.user
        passenger = Passenger.objects.get(user=request.user)
        routes = Ride.objects.filter(status="Available")
        paginator = Paginator(routes, 8)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)

        context = {
            'user': user,
            'passenger': passenger,
            'routes': routes,
            'page_obj': page_obj,
        }
        return render(request,'passenger/destinations.html',context)


@method_decorator(decoraters,name='dispatch')
class RideHistoryView(View):
    def get(self, request):
        user = request.user
        passenger = Passenger.objects.get(user=request.user)
        rides = Booking.objects.filter(passenger_no=passenger.passenger_no)
        paginator = Paginator(rides, 8)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)

        context = {
            'user': user,
            'passenger': passenger,
            'rides': rides,
            'page_obj': page_obj,
        }
        return render(request,'passenger/history.html',context)


@method_decorator(decoraters,name='dispatch')
class BookingView(View):
    def get(self, request,id):
        user = request.user
        passenger = Passenger.objects.get(user=request.user)
        route = Ride.objects.get(pk=id)
        driver = User.objects.get(username=route.driver_no)
        taxi = Taxi.objects.get(no_plate=route.taxi)
        d_img = Driver.objects.get(user=driver)

        context = {
            'user': user,
            'passenger': passenger,
            'route': route,
            'driver': driver,
            'taxi': taxi,
            'd_img': d_img,
        }
        return render(request, 'passenger/booktaxi.html', context)

@method_decorator(decoraters,name='dispatch')
class HireTaxiView(View):
    def get(self, request):
        user = request.user
        passenger = Passenger.objects.get(user=request.user)

        context = {
            'user': user,
            'passenger': passenger,
        }
        return render(request, 'passenger/hiretaxi.html',context)


    def post(self,request):
        datefor = request.POST['date']
        numdays = request.POST['days']

        passenger = Passenger.objects.get(user=request.user)

        if not Hiring.objects.filter(passenger=passenger, status="Unpaid").exists():
            exists = True
            while exists:

                digits = ""
                for i in range(0, 6):
                    value = randrange(0, 10)
                    digits = digits + str(value)

                reference = "H" + digits
                if not Hiring.objects.filter(reference=reference).exists():
                    if not Transactions.objects.filter(ride_no=reference).exists():
                        exists = False

            new_request = Hiring.objects.create(reference=reference,passenger=passenger,For=datefor,no_days=numdays)
            new_request.save()

            messages.success(request, 'Your hiring request has been sent. Wait for our communication.')
            messages.info(request, 'Your reference is '+ str(reference)+'.')
            return redirect('history')

        messages.error(request, 'You can not sent multiple hiring requests. Contacts us at 012 001 0001.')
        return redirect('hire-taxi')





