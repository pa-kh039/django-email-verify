from django.contrib import admin
from django.urls import path
from . import views

urlpatterns=[
    path('login',views.login_attempt, name='login_attempt'),
    path('register',views.register_attempt, name='register_attempt'),
    path('success',views.success, name='success'),
    path('token',views.token_send, name='token_send'),
    path('verify/<auth_token>',views.verify, name='verify'),
    path('error',views.error_page, name='error'),
    path('',views.home, name='home')
]