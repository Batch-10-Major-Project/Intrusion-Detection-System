import random
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import OTPVerification
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from ids.forms import RegistrationForm
from django.contrib.auth.models import User

@csrf_exempt
def register(request):
    if request.method == "POST":
        if request.POST['password'] != request.POST['confirm_password']:
            return HttpResponse('Incorrect Username or Password')

        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            user = User.objects.create_user(**form.cleaned_data)
            user.save()

    return render(request, 'register.html')
def send_otp(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, "signup.html", {"error": "User not found!"})

        otp_instance, created = OTPVerification.objects.get_or_create(user=user)
        otp_instance.generate_otp()

        send_mail(
            "Your OTP Code",
            f"Your OTP code is {otp_instance.otp}",
            "your-email@example.com",
            [email],
            fail_silently=False,
        )

        return redirect("verify_otp")
    
    return render(request, "signup.html")

@csrf_exempt
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('/home')

    return render(request, 'login1.html')


@login_required(login_url='/user_administration/login/')
def home(request):
    return render(request, 'index1.html')
    
@login_required(login_url='/user_administration/login/')
def about(request):
    return render(request, 'about.html')

@login_required(login_url='/user_administration/login/')
def contactus(request):
    return render(request, 'contactus.html')


@login_required(login_url='/user_administration/login/')
def prediction(request):
    return render(request, 'prediction.html')
