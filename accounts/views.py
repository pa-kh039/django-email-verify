from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import auth
from django.conf import settings
from django.core.mail import send_mail
from .models import *

import uuid

# Create your views here.
def home(request):
    return render(request,'home.html')

def login_attempt(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user_obj=User.objects.filter(username=username).first()
        if user_obj is None:
            messages.error('User does not exist')
            return redirect('/register')
        
        profile_obj=Profile.objects.filter(user=user_obj).first()

        if not profile_obj.is_verified:
            messages.warning('Verify your email first')
            return redirect('/login')
        
        user=auth.authenticate(username=username,password=password)
        if user is None:
            messages.warning('Invalid credentials')
            return redirect('/login')
        else:
            auth.login(request,user)
    return render(request,'login.html')

def register_attempt(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']

        try:
            if User.objects.filter(username=username).exists():
                messages.error(request,'username already taken')
                return redirect('register')
            if User.objects.filter(email=email).exists():
                messages.error(request,'email already taken')
                return redirect('register')
            
            user_obj= User.objects.create(username=username, email=email )
            user_obj.set_password(password)
            user_obj.save()

            auth_token=str(uuid.uuid4())

            profile_obj = Profile.objects.create(user=user_obj, auth_token=auth_token)
            profile_obj.save()
            send_mail_after_registration(email,auth_token)
            return redirect('/token')
        except Exception as e:
            print(e)

    return render(request,'register.html')

def success(request):
    return render(request,'success.html')

def verify(request,auth_token):
    try:
        profile_obj=Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if not profile_obj.is_verified:
                profile_obj.is_verified=True 
                profile_obj.save()
            messages.success(request,'email verified!')
            return redirect('/')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)

def token_send(request):
    return render(request,'token_send.html')

def send_mail_after_registration(email,token):
    subject="Your account needs to be verified"
    message= "Visit this link for verification: http://127.0.0.1:8000/verify/{}".format(token)
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject,message,email_from,recipient_list)
    return True

def error_page(request):
    return render(request,'error.html')