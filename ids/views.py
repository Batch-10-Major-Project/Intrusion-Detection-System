import random
import pyotp
import qrcode
import io
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import CustomUser
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
@login_required
def generate_qr(request):
    user = request.user
    if not user.two_factor_secret:
        user.generate_otp_secret()  # Generate a new secret if not set

    # Generate OTP URI for Google Authenticator
    otp_uri = pyotp.totp.TOTP(user.two_factor_secret).provisioning_uri(
        user.email, issuer_name="IDS Project"
    )

    # Generate QR code
    qr = qrcode.make(otp_uri)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type="image/png")
@login_required
def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        user = request.user

        totp = pyotp.TOTP(user.two_factor_secret)
        if totp.verify(entered_otp):
            login(request, user)  # Log in user after successful OTP
            return redirect("dashboard")  # Redirect to the main page
        else:
            return HttpResponse("Invalid OTP! Please try again.")

    return render(request, "verify_otp.html")


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
