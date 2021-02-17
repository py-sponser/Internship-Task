from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import AppointmentRequests
# Create your views here.
from .forms import AppointmentUpdate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse

def index(request):
    """Home Page"""
    return render(request,"index.html")


def book(request):
    """Handling user appointment information provided by user, saving it to database, sending emails to users"""
    if request.method == "POST": # getting all fields
        first_name = request.POST.get("first_name") 
        last_name = request.POST.get("last_name")
        email_address = request.POST.get("email_address")
        phone_code = request.POST.get("phone_code")
        phone_number = request.POST.get("phone_number")
        countries = request.POST.getlist("countries")
        company = request.POST.get("company")
        objective = request.POST.get("objective")
        details = request.POST.get("details")
        print(first_name,last_name,email_address,phone_code,phone_number,countries,company,objective,details)
        # if all fields not None and have value
        if first_name and last_name and email_address and phone_code and phone_number and countries and company and objective and details:
            try: # to check that phone number is not text, try to convert it to integar
                phone_number = int(phone_number)
            except: # if failed to be converted to integar
                messages.info(request,"Phone number field must be filled with numbers only.") # display this message for user
                return redirect("book") # reload the page
            mobile_number = phone_code + str(phone_number) # getting complete mobile number as string
            selected_countries = ", ".join(countries) # converting countries list to be saved as string
            print(selected_countries)
            if not AppointmentRequests.objects.filter(phone_number=mobile_number): # if a user tries to request an appointment with new info of mobile number and email address (not already exist in database)
                if not AppointmentRequests.objects.filter(email_address=email_address):

                    AppointmentRequests.objects.create(first_name=first_name,last_name=last_name,email_address=email_address,phone_number=mobile_number,
                            countries=selected_countries,company= company,objective=objective, details=details) # create an appointment


                    # send email to user
                    send_mail( 
                        subject=f"Service Provider Appointment",
                        message=f"""
                        Dear {first_name} {last_name},
                        [+] Your Info provided:
                        1- First name: {first_name}.
                        2- Last name: {last_name}.
                        3- Email address: {email_address}.
                        4- Phone number: {mobile_number}.
                        5- Countries: {selected_countries}.
                        6- Company: {company}.
                        7- Objective: {objective}.
                        8- Details:
                        {details}
                        \n
                        We will communicate with you as soon as possible.
                        """,
                        recipient_list=[email_address,],from_email="todotasks4000@gmail.com",fail_silently=False,
                    )
                    # send email to service provider agent
                    send_mail(
                        subject=f"A new requested Appointment by {first_name} {last_name}",
                        message=f"""
                        [+] Info provided:
                        1- First name: {first_name}.
                        2- Last name: {last_name}.
                        3- Email address: {email_address}.
                        4- Phone number: {mobile_number}.
                        5- Countries: {selected_countries}.
                        6- Company: {company}.
                        7- Objective: {objective}.
                        8- Details:
                        {details}
                        """,
                        recipient_list=["todotasks4000@gmail.com",],from_email="todotasks4000@gmail.com",fail_silently=False,
                    )
                    return redirect("confirm")

                else:
                    messages.info(request,"You have already sent a request, we will communicate you as soon as possible, we will handle any changes you want (if exist) when contact.")
                    return redirect("book") # reload the page

            else: # if user tries to request a new appointment using same mobile number
                messages.info(request,"You have already sent a request, we will communicate you as soon as possible, we will handle any changes you want (if exist) when contact.")
                return redirect("book") # reload the page
            


        else: # if any field is empty or None
            messages.info(request,"Please, fill empty fields")
            return redirect("book") # reload the page
            
    return render(request,"book_appointment.html")




def confirm(request):
    """Third page of confirmation"""
    return render(request,"confirm.html")

def user_login(request):
    """Login the user in"""
    if request.method == "POST": # if request method is POST: (which is sent by html form)
        # I don't use django form, I made and html form, recieving and validating data from here.
        username = request.POST.get("username") # getting username from the request.
        password_login = request.POST.get("password") # getting password from the request
        if User.objects.filter(username=username): # checking if the user is registered in the system or not by searching for its username in the db.
            user = authenticate(username=username, password=password_login) # authenticate the user, check for the credentials
            if user: # if credentials are true
                if user.is_active: # if user account is active (activated)
                    login(request, user) # log the user in, set the user object the user who logs in and create session for him.
                    return HttpResponseRedirect(reverse('dashboard')) # redirect to home page
                else: # if user is not active
                    messages.info(request, "Account hasn't been activated yet.") # create a message for the user.
                    return redirect("login") # redirect to the login page
            else: # if credentials is wrong
                messages.info(request, "Username or Password is incorrect.") # create a message for the user
                return redirect("login") # redirect to login page
        else: # if username is not found in db
            messages.info(request, "Account is not exist.") # create a message for the user
            return redirect("login") # redirect to login page
    else: # if request is not POST:
        return render(request, "login.html") # return rendering the request and the template.


@login_required(login_url="login") # only authenticated users can access it
def dashboard(request):
    """Lists all not completed appointments"""
    appointments = AppointmentRequests.objects.all().filter(completed=False)
    return render(request,"dashboard.html",{"appointments":appointments}) 

@login_required(login_url="login")
def update_appointment(request,pk):
    """Enable to update appointment details, especially assigning it as completed"""
    appointment = AppointmentRequests.objects.get(id=pk)
    form = AppointmentUpdate(instance=appointment)
    if request.method == "POST":
        form = AppointmentUpdate(request.POST,instance=appointment)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
        else:
            messages.info(request,"Invalid Data sent, Make sure you provided right data.")
            return redirect("update_appointment",pk=pk)
    else:
        return render(request,"update_appointment.html",{"form":form})


@login_required(login_url="login") # only authenticated users can access it
def completed_appointments(request):
    """Lists all completed appointments"""
    appointments = AppointmentRequests.objects.all().filter(completed=True)
    return render(request,"completed_appointments.html",{"appointments":appointments}) 
