from django.shortcuts import render, redirect
from django.views import View
from validate_email import validate_email
from django.contrib import messages
from django.contrib.auth.models import User,Group
from django.contrib import auth
from random import randrange
from passenger.models import Passenger,Booking

# Create your views here.
class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        messages.success(request, 'You Have Successfully Logged Out')
        return redirect('login')

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):

        username = request.POST['email']
        password = request.POST['password']

        if username and password:
            user= auth.authenticate(username=username,password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)


                    messages.success(request,"Welcome "+ user.first_name + " " + user.last_name+ ". You are now logged in.")



                    if user.groups.filter(name='owner').exists():
                        return redirect('dashboard')
                    elif user.groups.filter(name='driver').exists():
                        return redirect('homepage')
                    elif user.groups.filter(name='passenger').exists():
                        return redirect('passenger')
                    else:
                        messages.error(request,"You have not been assigned a role.")
                        return redirect('login')


                messages.success(request,"Account is not active. Please verify email.")
                return render(request, 'authentication/login.html')

            messages.success(request, "Invalid login credentials. Try again.")
            return render(request, 'authentication/login.html')

        messages.success(request, "Email and password fields cannot be empty.")
        return render(request, 'authentication/login.html')


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        name = request.POST['name']
        surname = request.POST['surname']
        email = request.POST['email']
        password = request.POST['password']
        con_pass = request.POST['password1']

        if password == con_pass:
            if not User.objects.filter(email=email).exists():

                if len(password) < 6:
                    messages.error(request, 'Password is too short.')
                    return render(request, 'authentication/register.html')

                if not validate_email(email):
                    messages.error(request, 'Invalid email address.')
                    return render(request, 'authentication/register.html')

                group = Group.objects.get(name='passenger')
                user = User.objects.create_user(username=email,email=email,first_name=name,last_name=surname)
                user.set_password(password)
                user.groups.add(group)
                user.save()


                user_model = User.objects.get(username=email)

                exists = True
                while exists:

                    digits = ""
                    for i in range(0, 8):
                        value = randrange(0, 10)
                        digits = digits + str(value)

                    passengerNo = digits
                    if not Passenger.objects.filter(passenger_no=passengerNo).exists():
                        if not Booking.objects.filter(passenger_no=passengerNo).exists():
                            exists = False

                new_passenger = Passenger.objects.create(user=user_model, passenger_no=passengerNo)
                new_passenger.save()

                messages.success(request, 'Account created successfully.')
                return redirect('login')

            messages.error(request, 'Email already exists..')
            return render(request, 'authentication/register.html')

        messages.error(request, 'Password does not match confirm password.')
        return render(request, 'authentication/register.html')
