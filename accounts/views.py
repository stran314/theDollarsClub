from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Sum
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from .models import *
from .forms import *
from .filters import *
from .decorators import *

# Create your views here.
@unauthenticated_user
def homePage(request):
    context = {}
    return render(request, 'accounts/home.html', context)

@unauthenticated_user
def membership(request):
    context = {}
    return render(request, 'accounts/membership.html', context)

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account created for ' + username)
            return redirect('login')
    context = {'form' : form}
    return render(request,'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('dashboard')
            else:
                return redirect('user-page')
        else:
            messages.info(request, 'Username OR password is incorrect')
    context = {}
    return render(request,'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'demo'])
def dashboard(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    total_sales = orders.filter(status='Fulfilled').count()
    total_revenue = orders.filter(status='Fulfilled').aggregate(prod_sum=Sum('product__price'))
    recent_customers = customers.order_by('-date_created')[:5]
    pending = orders.filter(status="Pending").count()
    reserved = orders.filter(status='Reserved').count()
    in_use = orders.filter(status='In Use').count()
    recent_orders = orders.order_by('-date_created')[:5]
    context = {'orders':orders, 'customers':customers,
	'total_customers' : total_customers, 'total_orders': total_orders,
    'total_sales' : total_sales, 'recent_customers' : recent_customers,
    'recent_orders' : recent_orders, 'total_revenue' : total_revenue,
    'pending' : pending, 'reserved' : reserved, 'in_use' : in_use}
    return render(request, 'accounts/dashboard.html', context)

@unauthenticated_user
def products(request):
    drinks = Product.objects.filter(tags__name="Alcohol")
    services = Product.objects.filter(category="Service")
    context = {'drinks' : drinks, 'services' : services,
    }
    return render(request, 'accounts/products.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'demo'])
def inventory(request):
    products = Product.objects.order_by('-date_created')
    context = {'products' : products}
    return render(request, 'accounts/inventory.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'demo'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all().order_by('-date_created')
    order_count = orders.count()
    reserv_count = orders.filter(status="Reserved").count()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer' : customer, 'orders' : orders,
    'order_count' : order_count, 'reserv_count' : reserv_count,
    'myFilter' : myFilter}
    return render(request, 'accounts/customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'demo'])
def createOrder(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context = {'form': form}
    return render(request, 'accounts/order_forms.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'demo'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context = {'form' : form}
    return render(request, 'accounts/order_forms.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'demo'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('dashboard')
    context = {'item' : order}
    return render(request, 'accounts/delete.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'demo'])
def allCustomer(request):
    customers = Customer.objects.order_by('-date_created')
    context = {'customers' : customers}
    return render(request, 'accounts/manage_customers.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'demo'])
def allOrder(request):
    orders = Order.objects.order_by('-date_created')
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {'orders' : orders, 'myFilter' : myFilter}
    return render(request, 'accounts/manage_orders.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'demo'])
def pendingOrders(request):
    orders = Order.objects.order_by('-date_created').filter(status='Pending')
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {'orders' : orders, 'myFilter' : myFilter}
    return render(request, 'accounts/manage_orders.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'demo'])
def reservedOrders(request):
    orders = Order.objects.order_by('-date_created').filter(status='Reserved')
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {'orders' : orders, 'myFilter' : myFilter}
    return render(request, 'accounts/manage_orders.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'demo'])
def inUseOrders(request):
    orders = Order.objects.order_by('-date_created').filter(status='In Use')
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {'orders' : orders, 'myFilter' : myFilter}
    return render(request, 'accounts/manage_orders.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'demo'])
def totalSales(request):
    orders = Order.objects.order_by('-date_created').filter(status='Fulfilled')
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {'orders' : orders, 'myFilter' : myFilter}
    return render(request, 'accounts/manage_orders.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all().order_by('-date_created')
    total_orders = orders.count()
    reservations = orders.filter(status='Reserved')
    reserved = reservations.count()
    pending_orders = orders.filter(status='Pending')
    pending = pending_orders.count()
    fulfilled = orders.filter(status='Fulfilled').count()
    total_spending = orders.filter(status='Fulfilled').aggregate(prod_sum=Sum('product__price'))
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {'orders' : orders, 'reserved' : reserved, 'fulfilled' : fulfilled,
    'pending_orders' : pending_orders, 'pending' : pending, 'reservations' : reservations,
    'myFilter' : myFilter, 'total_spending' : total_spending}
    return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    context = {'form' : form}
    return render(request, 'accounts/account_settings.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def makeReservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user-page')
    else:
        customer = request.user.customer
        data = {'customer' : customer, 'status' : 'Pending'}
        form = ReservationForm(initial=data)
    context = {'form' :form}
    return render(request, 'accounts/reservation.html', context)
