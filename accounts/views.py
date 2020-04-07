from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate ,login,logout
from .models import *
from .forms import OrderForm ,CreateUserForm,CustomerForm
from .filters import OrderFilter
from django.contrib  import messages 
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users,admins_only
from django.contrib.auth.models import Group,User

@unauthenticated_user
def registerPage(request):
    # CreateUserForm is customized user model 
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            # to pass the username in success msg 
            username = form.cleaned_data.get('username')
            #this is used to add user who sign up as customer
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            
            messages.success(request,'Account is created successfully for ' + username )

    context={'form':form}
    return render(request,'accounts/register.html',context)


@unauthenticated_user
def loginPage(request):    
    if request.method == 'POST':
        username = request.POST.get('username') #to get user data
        password = request.POST.get('password') #to get user data
        user = authenticate(request,username=username , password=password)

        if user is not None :
            login(request,user)   #login_access is given
            return redirect('home')
        else:
            messages.info(request,'Invalid Credentials !')

    return render(request,'accounts/login.html')

@login_required(login_url='login')
def logoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):

    #this is to get all specific orders of user
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()   #count() to get the count of total orders
    delivered = orders.filter(status = 'Delivered').count() #to get count of orders based on status
    pending = orders.filter(status = 'Pending').count()  #to get count of orders based on status
    context = { 'orders':orders,'total_orders':total_orders,'delivered':delivered,'pending':pending}
    return render(request,'accounts/user.html',context)

@login_required(login_url='login')

def home(request):
    # all data is fetched
    customers = Customer.objects.all()
    products = Product.objects.all()
    orders = Order.objects.all()

    total_orders = orders.count()   #count() to get the count of total orders
    delivered = orders.filter(status = 'Delivered').count() #to get count of orders based on status
    pending = orders.filter(status = 'Pending').count()  #to get count of orders based on status

    
    context ={'customers':customers,'products':products,'orders':orders,'total_orders':total_orders,'delivered':delivered,'pending':pending}
    return render(request,'accounts/dashboard.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def product(request):
    products = Product.objects.all()
    context ={'products':products}

    return render(request,'accounts/product.html',context)
 
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request,pk):
    customer = Customer.objects.get(id=pk)  #to get user using specific id
    
    
    orders = customer.order_set.all() 
    order_count = orders.count()

    # filters that are created in filters.py are used here
    myFilter = OrderFilter(request.GET,queryset = orders)
    orders = myFilter.qs
    context = {'customer':customer,'orders':orders,'order_count':order_count ,'myFilter':myFilter}
    return render(request,'accounts/customer.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_order(request ,pk):
    customer= Customer.objects.get(id=pk)
    # to set default customer
    form = OrderForm(initial={'customer':customer})  
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render (request,'accounts/create_order.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_order(request,pk): 
    order = Order.objects.get(id=pk)
    # instance =  order to get prefilled form
    form = OrderForm(instance = order)  
    if request.method == "POST":
        # instance  # to get prefilled order form to update
        form = OrderForm(request.POST,instance = order)  
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render (request,'accounts/update_order.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request,pk): 
    # order is deleted using getting order id
    order = Order.objects.get(id=pk).delete()
    return redirect('/')
   

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def setting(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == "POST":
        form = CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request,'accounts/settings.html',context)