from django.urls import path
from .views import contact,index

urlpatterns=[
    path('',contact),
]

urlpatterns=[
    path('',index),
]