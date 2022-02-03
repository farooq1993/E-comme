from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from unagaapp .models import Product, Banner, Left_Banner, Arrivals, Right_Banner, Customer_Register


# home page view:
def base(request):
    banner = Banner.objects.all()
    leftbanners = Left_Banner.objects.all()
    rightbanners = Right_Banner.objects.all()
    products = Product.objects.all()
    arrivals = Arrivals.objects.all()
    return render(request, 'base_cutomer.html',  {"banner": banner, "leftbanners": leftbanners, "rightbanners": rightbanners, "products": products, "arrivals": arrivals})


def all_product(request):
    product = Product.objects.all()
    return render(request, "all-products.html", {"product": product})


def product_details(request, id):
    products = Product.objects.get(id=id)
    return render(request, 'product-details.html', {"products": products})


def customer_register(request):
    if request.method == "POST":
        customer_username = request.POST['customer_username']
        customer_email = request.POST['customer_email']
        customer_password = request.POST['customer_password']
        customer_confirm_password = request.POST['customer_confirm_password']

        if customer_password == customer_confirm_password:
            if Customer_Register.objects.filter(customer_username=customer_username).exists():
                messages.info(request, 'Username Taken already')
                return redirect('/customer_register')
            elif Customer_Register.objects.filter(customer_email=customer_email).exists():
                messages.info(request, 'Email Taken already')
                return redirect('/customer_register')
            else:
                Customer_Register(customer_username=customer_username, customer_email=customer_email, customer_password=customer_password,
                                  customer_confirm_password=customer_confirm_password).save()
                messages.info(request, "customer registered successfully...")
                return redirect('/customer_login')
        else:
            messages.info(request, 'Password not matching')
            return redirect('/customer_register')
    else:
        return render(request, 'customer-register.html')


def customer_login(request):
    banner = Banner.objects.all()
    leftbanners = Left_Banner.objects.all()
    rightbanners = Right_Banner.objects.all()
    products = Product.objects.all()
    arrivals = Arrivals.objects.all()
    context = {"banner": banner, "leftbanners": leftbanners,
               "rightbanners": rightbanners, "products": products, "arrivals": arrivals}
    if request.method == "POST":
        try:
            Customerdetails = Customer_Register.objects.get(
                customer_username=request.POST["customer_username"], customer_password=request.POST["customer_password"])
            request.session['customer_username'] = Customerdetails.customer_username
            return render(request, 'base_cutomer.html', context)
        except Customer_Register.DoesNotExist as e:
            messages.success(request, 'Incorrect password')
    return render(request, 'customer-login.html')
