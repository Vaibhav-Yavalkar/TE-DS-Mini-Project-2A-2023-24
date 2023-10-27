from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
from iFeelsApp.models import Contact, Sign_up
from django.contrib import messages
from django.contrib.auth import authenticate, login

# Create your views here.
def index_function(request):
    return render(request, 'index.html')
    # return HttpResponse("This is Sign_in Page.")

# Users: Username: himanshumaurya0007 Password: Design%^&000
# Username; faizftw Password: Faiz$2109

def sign_in_function(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(username, password)

        # check if user has entered correct credentials
        user = authenticate(username=username, password=password)

        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            return redirect("/home")

        else:
            # No backend authenticated the credentials
            return render(request, 'sign_in.html')

    return render(request, 'sign_in.html')

def sign_up_function(request):
    if request.method == "POST":
        # Get data from the form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        security_question = request.POST.get('security_question')
        security_question_answer = request.POST.get('security_question_answer')
        password = request.POST.get('password')
        
        # Check if the username already exists
        if Sign_up.objects.filter(username=username).exists():
            # If the username exists, show a message and redirect to the sign-up page
            messages.error(request, "Username already exists. Please choose a different username.")
            return redirect('/sign_up')  # Assuming 'signup' is the URL name for your sign-up page
        
        # If the username is unique, create a new User instance and save it to the database
        sign_up = Sign_up(first_name=first_name, last_name=last_name, email=email, username=username, security_question=security_question, security_question_answer=security_question_answer, password=password)
        sign_up.save()
        
        messages.success(request, "Sign up, successful!!")

    return render(request, 'sign_up.html')

from django.contrib.auth.models import User  # Assuming you're using Django's built-in User model

def forgot_password_function(request):
    if request.method == 'POST':
        # Get the username from the form
        username = request.POST['username']
        security_question_answer = request.POST['security_question_answer']

        # Check if the user exists
        try:
            user = User.objects.get(username=username)
            # Get user details like first_name, last_name, email, and security_question from the user object
            first_name = user.first_name
            last_name = user.last_name
            email = user.email
            security_question = user.security_question  # Replace 'security_question' with the actual field name in your model

            # Check if the user answered the security question correctly
            if request.POST['security_question_answer'] == user.security_question_answer:  # Replace 'security_answer' with the actual field name in your model
                # Provide the user's password in a secure way (e.g., email)
                password = user.password
                return render(request, 'forgot_password.html', {'password': password})
            else:
                messages.error(request, "Incorrect security question's answer!!")
                # return render(request, 'forgot_password.html', {'error_message': 'Incorrect security answer'})
        except User.DoesNotExist:
             messages.error(request, "User not found!!")

    return render(request, 'forgot_password.html')


def home_function(request):
    return render(request, 'home.html')

def contact_function(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        desc = request.POST.get('desc')
        contact = Contact(name=name, email=email, desc=desc, date=datetime.today())
        contact.save()
        messages.success(request, "Your message has been sent!!")
        
    return render(request, 'contact.html')



def about_function(request):
    return render(request, 'about.html')
