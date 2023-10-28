from django.urls import path 
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('search/', views.search_movies, name="Register_Page"),
    path('Login/', views.Login, name="Login_Page"),

]