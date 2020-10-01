from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
# Create your views here.
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, cartData
from validate_email import validate_email
# Create your views here.
def usernameValidation(request):
    data = json.loads(request.body)
    username = data['username']
    if not str(username).isalnum():
        return JsonResponse({'username_error': 'Username should only alphanumeric characters'}, status=200)
    if User.objects.filter(username=username).exists():
        return JsonResponse({'username_error': 'Username is already taken,choose another one'}, status=400)
    return JsonResponse({'username_valid': True})

def emailValidation(request):
    data = json.loads(request.body)
    email = data['email']
    if not validate_email(email):
        return JsonResponse({'email_error': 'Email is invalid, set your correct email address'}, status=400)
    if User.objects.filter(email=email):
        return JsonResponse({'email_error': 'Sorry, email address is already used, try another one'}, status=400)
    return JsonResponse("email validatioon", safe=False)


def register(request):
    if request.user.is_authenticated:
        return redirect('product_list')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            password = request.POST['password']
            context = {'fieldValue': request.POST}
            if not User.objects.filter(username=username).exists():
                if not User.objects.filter(email=email).exists():
                    if len(password)<8:
                        messages.error(request, 'password too short,it have to be minimun 8 characters')
                        return render(request, 'account/register.html', context)
                    if len(username)<5:
                        messages.error(request, 'your username less than 5 characters, try again')
                        return render(request, 'account/register.html', context)
                    user = User.objects.create_user(username=username, email=email)
                    user.first_name = fname
                    user.last_name = lname
                    user.set_password(password)
                    user.save()
                    messages.success(request, 'your account has been successfully created')
                    return redirect('login')
        return render(request, 'account/register.html')





def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order , created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse("it was added", safe=False)

def product_list(request):
    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()
    context = { 'products': products , 'cartItems': cartItems}
    return render(request, 'home/product_home.html', context)

def cart_list(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = { 'items': items, 'order':order, 'cartItems':cartItems }
    return render(request, 'home/cart.html', context)

def checkout(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = { 'items': items, 'order':order, 'cartItems': cartItems }
    return render(request, 'home/checkout.html', context )

def product_details(request):
    return render(request, 'home/product_details.html')

def proceOrder(request):
    #print( 'data:', request.body)
    transction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if  request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        print('user is not log in')
        name = data['form']['name']
        email = data['form']['email']
        cookieData = cookieCart(request)
        items = cookieData['items']
        customer, created = Customer.objects.get_or_create(
             email=email,

        )
        customer.name = name
        customer.save()
        order = Order.objects.create(
            customer=customer,
            complete=False,
        )
        for item in items:
            product = Product.objects.get(id=item['product']['id'])
            orderItem = OrderItem.objects.create(
                product=product,
                order = order,
                quantity=item['quantity']
            )

    total = float(data['form']['total'])
    order.transaction_id = transction_id
    if total == order.get_item_total_price:
        order.complete = True
    order.save()
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],

        )
    return JsonResponse("payment completed", safe=False)
