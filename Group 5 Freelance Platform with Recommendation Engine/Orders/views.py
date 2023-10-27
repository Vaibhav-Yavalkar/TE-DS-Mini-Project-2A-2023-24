from django.shortcuts import render
from .models import Orders

# Create your views here.
def order_view(request):
    user = request.user.username
    orders = Orders.objects.filter(buyer=user)
    return render(request, 'Orders/orders.html', {'orders': orders})