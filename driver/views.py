from django.shortcuts import render,redirect,reverse
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Taxi,Driver,Destination
from passenger.models import Ride,Passenger,Booking
from owner.models import Transactions
from django.core.paginator import Paginator
from random import randrange
from django.contrib.auth.decorators import login_required,user_passes_test
from django.utils.decorators import method_decorator

decoraters = [login_required(login_url='/auth/login'),user_passes_test(lambda u: u.groups.filter(name='driver').exists())]

# Create your views here.
@method_decorator(decoraters,name='dispatch')
class MarkDoneView(View):
    def get(self,request,id):
        mark_route = Ride.objects.get(pk=id)
        mark_route.status = "Complete"
        mark_route.save()

        messages.success(request, "Route done")
        return redirect('homepage')


@method_decorator(decoraters,name='dispatch')
class HomepageView(View):
    def get(self, request):
        user = request.user
        driver = Driver.objects.get(user=request.user)
        routes = Ride.objects.filter(status="Available")[:5]
        ongoings = Ride.objects.filter(driver_no=driver.driver_no,status="On going")
        context = {
            'user': user,
            'driver': driver,
            'routes': routes,
            'ongoings': ongoings,
        }
        return render(request, 'driver/index.html',context)


@method_decorator(decoraters,name='dispatch')
class RoutemanagerView(View):
    def get(self, request,id):
        user = request.user
        driver = Driver.objects.get(user=request.user)
        route = Ride.objects.get(pk=id)
        passengers = Booking.objects.filter(ride_no=route)
        if Transactions.objects.filter(ride_no=route.ride_no).exists():
            transact = Transactions.objects.get(ride_no=route.ride_no)
        else:
            transact =None
        numSeats = int(driver.taxi.seats) - len(passengers)

        context = {
            'user': user,
            'driver': driver,
            'route': route,
            'id': id,
            'passengers': passengers,
            'transact': transact,
            'numSeats': numSeats,
        }
        return render(request, 'driver/manageroute.html',context)

    def post(self,request,id):
        route = Ride.objects.get(pk=id)
        driver = Driver.objects.get(user=request.user)
        name = request.POST['name']
        surname = request.POST['surname']
        p_contact = request.POST['pcontact']
        contactPerson = request.POST['contact-person']
        e_contact = request.POST['econtact']

        passNo = "Walk-IN"
        numPass = len(Booking.objects.filter(ride_no=route))
        taxiSeats = int(driver.taxi.seats)

        if numPass < taxiSeats:

            addpass = Booking.objects.create(ride_no=route, passenger_no=passNo, name=name,
                                          surname=surname, p_contacts=p_contact,
                                          contact_person=contactPerson, e_contacts=e_contact)

            addpass.save()
            messages.success(request, "Passenger added succesfully.")
            return redirect('manage-route', route.id)
        else:
            messages.error(request, "Taxi full")
            return redirect('manage-route', route.id)



@method_decorator(decoraters,name='dispatch')
class RouteView(View):

    def get(self,request):
        user = request.user
        driver = Driver.objects.get(user=request.user)
        destinations = Destination.objects.all()

        context = {
            'user': user,
            'driver': driver,
            'destinations': destinations,
        }
        return render(request, 'driver/route.html',context)


    def post(self, request):
        destFrom = request.POST['from']
        destTo = request.POST['to']
        driverUser = request.user
        driver = Driver.objects.get(user=driverUser)

        if destFrom != destTo:
            exists = True
            while exists:

                digits = ""
                for i in range(0, 6):
                    value = randrange(0, 10)
                    digits = digits + str(value)

                rideNo = "T" + digits
                if not Ride.objects.filter(ride_no=rideNo).exists():
                    if not Transactions.objects.filter(ride_no=rideNo).exists():
                        exists = False

            if Ride.objects.filter(driver_no=driver.driver_no,status="Available").exists():
                messages.error(request, "You have a route already available")
                return redirect('add-route-d')

            if Ride.objects.filter(driver_no=driver.driver_no,status="On going").exists():
                    messages.error(request,"You have a route already available")
                    return redirect('add-route-d')

            travel = Ride.objects.create(ride_no=rideNo, d_from=destFrom, d_to=destTo, driver_no=driver.driver_no,
                                     taxi=driver.taxi.no_plate)
            travel.save()

            messages.success(request, 'Successfully added route.')
            return redirect('homepage')

        messages.error(request, 'You cannot choose the same location for both from and to.')
        return redirect('add-route-d')


@method_decorator(decoraters,name='dispatch')
class AllRoutesView(View):

    def get(self, request):
        user = request.user
        driver = Driver.objects.get(user=request.user)
        routes = Ride.objects.filter(status="Available")
        paginator = Paginator(routes, 8)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)

        context = {
            'user': user,
            'driver': driver,
            'routes': routes,
            'page_obj': page_obj,
        }
        return render(request,'driver/allroutes.html',context)


@method_decorator(decoraters,name='dispatch')
class AddTransactionView(View):
    def post(self,request,id):
        amt = request.POST['amount']

        route = Ride.objects.get(pk=id)

        if route.status == "Available":

            route.status = "On going"
            route.save()
            category = "Transport"

            transact = Transactions.objects.create(ride_no=route.ride_no,driver_no=route.driver_no,amount=amt,category=category)
            transact.save()

            messages.success(request,"Information captured")
            return redirect('manage-route',route.id)
        else:
            messages.error(request, "Already marked paid")
            return redirect('manage-route',route.id)


@method_decorator(decoraters,name='dispatch')
class DeleteRouteView(View):
    def get(self,request,id):
        del_route = Ride.objects.get(pk=id)
        del_route.delete()

        messages.success(request, "Route deleted successfully")
        return redirect('all-routes')



@method_decorator(decoraters,name='dispatch')
class RemovePassengerView(View):
    def get(self,request,id):
        del_pass = Booking.objects.get(pk=id)
        route = del_pass.ride_no
        del_pass.delete()

        messages.success(request, "Passenger removed successfully")
        return redirect('manage-route',route.id)


@method_decorator(decoraters,name='dispatch')
class AddRegisteredView(View):
    def post(self,request,id):
        pass_no = request.POST['passenger']


        route = Ride.objects.get(pk=id)
        driver = Driver.objects.get(driver_no=route.driver_no)

        if route.status == "Available":
            if Passenger.objects.filter(passenger_no=pass_no).exists():
                if not Booking.objects.filter(ride_no=route,passenger_no=pass_no).exists():
                    numPass = len(Booking.objects.filter(ride_no=route))
                    taxiSeats = int(driver.taxi.seats)
                    if numPass < taxiSeats:

                        passenger = Passenger.objects.get(passenger_no=pass_no)

                        add_pass = Booking.objects.create(ride_no=route,passenger_no=passenger.passenger_no,name=passenger.user.first_name,
                                                  surname=passenger.user.last_name,p_contacts=passenger.p_contacts,
                                                  contact_person=passenger.contact_person,e_contacts=passenger.e_contacts)

                        add_pass.save()
                        messages.success(request,"Passenger added succesfully.")
                        return redirect('manage-route',route.id)
                    else:
                        messages.error(request, "Taxi full")
                        return redirect('manage-route', route.id)

                else:
                    messages.error(request, "Passenger already captured")
                    return redirect('manage-route',route.id)

            else:
                messages.error(request, "Passenger number does not exists.")
                return redirect('manage-route',route.id)

        else:
            messages.error(request, "You cannot add passenger to already closed destinations")
            return redirect('manage-route',route.id)

