from django.shortcuts import render,redirect
from django.views import View
from driver.models import Taxi, Destination, Driver
from passenger.models import Ride,Passenger,Hiring
from .models import Transactions,ToDoList,Owner
from django.contrib import messages
from django.contrib.auth.models import User,Group
from random import randrange
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required,user_passes_test
from django.utils.decorators import method_decorator

decoraters = [login_required(login_url='/auth/login'),user_passes_test(lambda u: u.groups.filter(name='owner').exists())]


# Create your views here.

@method_decorator(decoraters,name='dispatch')
class DestView(View):
    def get(self, request):
        user = request.user
        owner = Owner.objects.get(user=request.user)
        routes = Ride.objects.filter(status="Available")
        paginator = Paginator(routes, 8)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)

        context = {
            'user': user,
            'owner': owner,
            'routes': routes,
            'page_obj': page_obj,
        }

        return render(request, 'owner/dest.html', context)

@method_decorator(decoraters,name='dispatch')
class DeleteTaskView(View):
    def get(self,request,id):
        del_task = ToDoList.objects.get(pk=id)
        del_task.delete()

        messages.success(request, "Task deleted successfully")
        return redirect('todolist')


@method_decorator(decoraters, name='dispatch')
class DeleteDriverView(View):
    def get(self, request, id):
        driver = Driver.objects.get(pk=id)
        del_driver = driver.user
        del_driver.delete()

        messages.success(request, "Driver deleted successfully")
        return redirect('view-drivers')


@method_decorator(decoraters, name='dispatch')
class DeleteTaxiView(View):
    def get(self, request, id):
        del_taxi = Taxi.objects.get(pk=id)
        del_taxi.delete()

        messages.success(request, "Taxi deleted successfully")
        return redirect('view-taxis')


@method_decorator(decoraters, name='dispatch')
class DeleteRequestView(View):
    def get(self, request, id):
        del_request = Hiring.objects.get(pk=id)
        del_request.delete()

        messages.success(request, "Hiring request deleted successfully")
        return redirect('hire-requests')



@method_decorator(decoraters,name='dispatch')
class MarkTaskView(View):
    def get(self,request,id):
        del_task = ToDoList.objects.get(pk=id)

        if del_task.status == "Not Done":
            del_task.status = "Done"
        else:
            del_task.status = "Not Done"

        del_task.save()
        messages.success(request, "Task marked successfully")
        return redirect('todolist')

@method_decorator(decoraters,name='dispatch')
class TodolistView(View):
    def get(self, request):
        user = request.user
        owner = Owner.objects.get(user=request.user)
        todolist = ToDoList.objects.all()

        context = {
            'user': user,
            'owner': owner,
            'todolist': todolist,
        }
        return render(request, 'owner/todolist.html', context)

    def post(self,request):
        task = request.POST['task']

        new_task = ToDoList.objects.create(task=task)
        new_task.save()

        messages.success(request, "Task successfully added")
        return redirect('todolist')


@method_decorator(decoraters,name='dispatch')
class DashBoardView(View):
    def get(self, request):
        user = request.user
        owner = Owner.objects.get(user=request.user)
        routes = Ride.objects.filter(status="Available")[:5]
        hireRequests = Hiring.objects.filter(status="Unpaid")[:5]
        todolist = ToDoList.objects.all()[:5]
        hiring = Transactions.objects.filter(category='Hire')
        transports = Transactions.objects.filter(category='Transport')

        passengers = len(Passenger.objects.all())
        drivers = len(Driver.objects.all())

        hireamt = 0
        transamt = 0
        if hiring:
            for hire in hiring:
                hireamt+=hire.amount
        if transports:
            for transport in transports:
                transamt+=transport.amount


        context = {
            'user': user,
            'owner': owner,
            'routes': routes,
            'hireRequests': hireRequests,
            'todolist': todolist,
            'passengers': passengers,
            'drivers': drivers,
            'hireamt': hireamt,
            'transamt': transamt,
        }
        return render(request, 'owner/index.html', context)

    def post(self,request):
        task = request.POST['task']

        new_task = ToDoList.objects.create(task=task)
        new_task.save()

        messages.success(request, "Task successfully added")
        return redirect('dashboard')

@method_decorator(decoraters,name='dispatch')
class AddRouteView(View):
    def get(self, request):
        user = request.user
        owner = Owner.objects.get(user=request.user)

        context = {
            'user': user,
            'owner': owner,
        }
        return render(request, 'owner/addroute.html',context)

    def post(self,request):
        nam = request.POST['place']

        if not Destination.objects.filter(name=nam).exists():

            place = Destination.objects.create(name=nam)
            place.save()

            messages.success(request, 'Successfully added destination.')
            return redirect('add-route')
        else:
            messages.error(request, 'Destination already exists')
            return redirect('add-route')


@method_decorator(decoraters,name='dispatch')
class AddDestination(View):
    def get(self, request):
        user = request.user
        owner = Owner.objects.get(user=request.user)
        destinations = Destination.objects.all()
        drivers = User.objects.filter(groups__name="driver")

        context = {
            'user': user,
            'owner': owner,
            'destinations': destinations,
            'drivers': drivers,
        }
        return render(request, 'owner/adddesti.html',context)

    def post(self,request):
        destFrom = request.POST['from']
        destTo = request.POST['to']
        driverNo = request.POST['driver'][0:9]

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

            driver = Driver.objects.get(driver_no=driverNo)

            travel = Ride.objects.create(ride_no=rideNo,d_from=destFrom,d_to=destTo,driver_no=driver.driver_no,taxi=driver.taxi.no_plate)
            travel.save()

            messages.success(request, 'Successfully added route.')
            return redirect('dashboard')

        messages.error(request, 'You cannot choose the same location for both from and to.')
        return redirect('add-destination')

@method_decorator(decoraters,name='dispatch')
class PassengersView(View):
    def get(self, request):
        user = request.user
        owner = Owner.objects.get(user=request.user)
        passengers = Passenger.objects.all()
        paginator = Paginator(passengers, 8)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)

        context = {
            'user': user,
            'owner': owner,
            'passengers': passengers,
            'page_obj': page_obj,
        }
        return render(request, 'owner/view-passengers.html',context)

@method_decorator(decoraters,name='dispatch')
class DriversView(View):
    def get(self, request):
        user = request.user
        owner = Owner.objects.get(user=request.user)
        drivers = Driver.objects.all()
        paginator = Paginator(drivers, 8)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)

        context = {
            'user': user,
            'owner': owner,
            'drivers': drivers,
            'page_obj': page_obj,
        }
        return render(request, 'owner/view-drivers.html',context)

@method_decorator(decoraters,name='dispatch')
class TaxisView(View):
    def get(self, request):
        user = request.user
        owner = Owner.objects.get(user=request.user)
        taxis = Taxi.objects.all()
        paginator = Paginator(taxis, 8)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)

        context = {
            'user': user,
            'owner': owner,
            'taxis': taxis,
            'page_obj': page_obj,
        }
        return render(request, 'owner/view-taxis.html',context)


    def post(self, request):

        numplate = request.POST['numplate']
        model = request.POST['model']
        color = request.POST['color']
        numseats = request.POST['numseats']


        if not Taxi.objects.filter(no_plate=numplate).exists():

            taxi = Taxi.objects.create(no_plate=numplate,model=model,color=color,seats=numseats)
            taxi.save()

            messages.success(request,'Successfully added taxi.')
            return redirect('view-taxis')
        else:
            messages.error(request, 'Taxi already exists')
            return redirect('view-taxis')

@method_decorator(decoraters,name='dispatch')
class HireRequestView(View):
    def get(self, request):
        user = request.user
        owner = Owner.objects.get(user=request.user)
        hireRequests = Hiring.objects.filter(status="Unpaid")
        paginator = Paginator(hireRequests, 8)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)

        context = {
            'user': user,
            'owner': owner,
            'page_obj': page_obj,
        }
        return render(request, 'owner/hiringrequest.html',context)

@method_decorator(decoraters,name='dispatch')
class RequestVieW(View):
    def get(self, request,id):
        user = request.user
        owner = Owner.objects.get(user=request.user)
        hireRequest = Hiring.objects.get(pk=id)
        drivers = Driver.objects.all()
        if Transactions.objects.filter(ride_no=hireRequest.reference).exists():
            transaction = Transactions.objects.get(ride_no=hireRequest.reference)
            myDriver = Driver.objects.get(driver_no=transaction.driver_no)

        else:
            transaction = None
            myDriver = None
        context = {
            'user': user,
            'owner': owner,
            'hireRequest': hireRequest,
            'drivers': drivers,
            'transaction': transaction,
            'myDriver': myDriver,
        }

        return render(request, 'owner/request.html',context)

    def post(self,request,id):
        category = "Hire"
        paid = "Paid"
        hireRequest = Hiring.objects.get(pk=id)
        driverNo = request.POST['driver'][0:9]
        amt = request.POST['amount']

        transaction = Transactions.objects.create(ride_no=hireRequest.reference,driver_no=driverNo,amount=amt,category=category)
        transaction.save()

        hireRequest.status = paid
        hireRequest.save()

        messages.success(request,"Hire request marked added to database.")
        return redirect('hire-requests')


@method_decorator(decoraters,name='dispatch')
class AddDriverView(View):

   def get(self, request):
       user = request.user
       owner = Owner.objects.get(user=request.user)
       taxis = Taxi.objects.all()

       context = {
            'user': user,
           'owner': owner,
            'taxis': taxis,
        }
       return render(request, 'owner/add-driver.html', context)


   def post(self,request):
       name = request.POST['name']
       surname = request.POST['surname']
       contacts = request.POST['contacts']
       taxi = request.POST['taxi']
       password = request.POST['password']
       con_pass = request.POST['password1']

       if password == con_pass:
           if len(password) > 5:
               exists = True
               while exists:

                   digits = ""
                   for i in range(0, 8):
                       value = randrange(0, 10)
                       digits = digits + str(value)

                   driverNo ="D"+ digits
                   if not Driver.objects.filter(driver_no=driverNo).exists():
                       if not User.objects.filter(username=driverNo).exists():
                           if not Transactions.objects.filter(driver_no=driverNo).exists():
                               exists = False

               group = Group.objects.get(name='driver')
               user = User.objects.create_user(username=driverNo, first_name=name, last_name=surname)
               user.set_password(password)
               user.groups.add(group)
               user.save()

               user_model = User.objects.get(username=driverNo)
               taxi_model = Taxi.objects.get(no_plate=taxi)

               if request.FILES.get('image') == None:
                   new_driver = Driver.objects.create(user=user_model, driver_no=driverNo,contacts=contacts,taxi=taxi_model)

               if request.FILES.get('image') != None:
                   img = request.FILES.get('image')
                   new_driver = Driver.objects.create(user=user_model, driver_no=driverNo, contacts=contacts, img=img,taxi=taxi_model)

               new_driver.save()

               messages.success(request, "Driver successfully added")
               messages.success(request, "Driver Username is "+ str(driverNo))
               return redirect('view-drivers')

           messages.error(request, "Password is too short. Try again.")
           return redirect('add-driver')

       messages.error(request, "Passwords do not match. Try again.")
       return redirect('add-driver')

@method_decorator(decoraters,name='dispatch')
class EditDriverView(View):

   def get(self, request,id):
       user = request.user
       owner = Owner.objects.get(user=request.user)
       taxis = Taxi.objects.all()
       driver = Driver.objects.get(pk=id)
       transactions = Transactions.objects.filter(driver_no=driver.driver_no)
       paginator = Paginator(transactions, 8)
       page_number = request.GET.get('page')
       page_obj = Paginator.get_page(paginator, page_number)

       context = {
            'user': user,
           'owner': owner,
            'taxis': taxis,
            'driver': driver,
           'page_obj': page_obj,
        }
       return render(request, 'owner/edit-driver.html', context)


   def post(self,request,id):

       name = request.POST['name']
       surname = request.POST['surname']
       contacts = request.POST['contacts']
       taxi = request.POST['taxi']

       driver = Driver.objects.get(pk=id)

       user_model = User.objects.get(username=driver.user.username)
       taxi_model = Taxi.objects.get(no_plate=taxi)

       user_model.first_name = name
       user_model.last_name = surname
       user_model.save()

       if request.FILES.get('image') == None:
           driver.contacts = contacts
           driver.taxi = taxi_model

       if request.FILES.get('image') != None:
           img = request.FILES.get('image')
           driver.img = img
           driver.contacts = contacts
           driver.taxi = taxi_model

       driver.save()
       messages.success(request, "Driver successfully updated")
       return redirect('view-drivers')


@method_decorator(decoraters,name='dispatch')
class RouteView(View):
    def get(self, request, id):
        user = request.user
        owner = Owner.objects.get(user=request.user)
        route = Ride.objects.get(pk=id)
        driver = User.objects.get(username=route.driver_no)
        taxi = Taxi.objects.get(no_plate=route.taxi)
        d_img = Driver.objects.get(user=driver)

        context = {
            'user': user,
            'owner': owner,
            'route': route,
            'driver': driver,
            'taxi': taxi,
            'd_img': d_img,
        }
        return render(request, 'owner/view-route.html',context)


@method_decorator(decoraters,name='dispatch')
class PassProfileView(View):
    def get(self, request,id):
        user = request.user
        owner = Owner.objects.get(user=request.user)
        passenger = User.objects.get(pk=id)
        pass_info = Passenger.objects.get(user=passenger)

        context = {
            'user': user,
            'owner': owner,
            'passenger': passenger,
            'pass_info': pass_info,
        }
        return render(request, 'owner/view-profile.html', context)


@method_decorator(decoraters,name='dispatch')
class EditTaxiView(View):
    def get(self, request,id):
        user = request.user
        owner = Owner.objects.get(user=request.user)
        taxi = Taxi.objects.get(pk=id)

        context = {
            'user': user,
            'owner': owner,
            'taxi': taxi,
        }
        return render(request, 'owner/edit-taxi.html', context)

    def post(self, request,id):
        numplate = request.POST['numplate']
        model = request.POST['model']
        color = request.POST['color']
        numseats = request.POST['numseats']
        taxi = Taxi.objects.get(pk=id)

        if not Taxi.objects.filter(no_plate=numplate).exists():

            messages.error(request,"You cannot change number plate. Add a new taxi.")
            return redirect('view-taxis')
        else:
            taxi.model = model
            taxi.color = color
            taxi.seats = numseats
            taxi.save()

            messages.success(request, 'Successfully updated taxi.')
            return redirect('view-taxis')


@method_decorator(decoraters,name='dispatch')
class TransactionView(View):
    def get(self, request):
        user = request.user
        owner = Owner.objects.get(user=request.user)
        transactions = Transactions.objects.all()
        paginator = Paginator(transactions, 8)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)

        context = {
            'user': user,
            'owner': owner,
            'page_obj': page_obj,
        }
        return render(request, 'owner/transaction.html', context)
