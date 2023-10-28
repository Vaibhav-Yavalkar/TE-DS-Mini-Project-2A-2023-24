from django.contrib import admin
from django.urls import path
from iFeelsApp import views

urlpatterns = [
    path("", views.index_function, name='index'),
    path("sign_in", views.sign_in_function, name='sign_in'),
    path("sign_up", views.sign_up_function, name='sign_up'),
    path("forgot_password", views.forgot_password_function, name='forgot_password'),
    path("home", views.home_function, name='home'),
    path("contact", views.contact_function, name='contact'),
    path("about", views.about_function, name='about'),
]