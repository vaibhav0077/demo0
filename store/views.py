from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from .models import Customer
from django.contrib.auth.hashers import make_password, check_password
from store.models import Category, Product, Customer, Order
from django.views import View
from store.middleware.auth import auth_middleware
from django.utils.decorators import method_decorator


class HomeView(View):
    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        categoryId = request.GET.get('category')
        # print(request.session['email'])
        # print(request.session['customer_id'])

        if categoryId:
            products = Product.all_product_category_by_id(categoryId)

        else:
            products = Product.all_product()

        categories = Category.all_category
        return render(request, 'home.html', {'products':products, 'categories': categories})


    def post(self, request):
        product = request.POST.get('product')
        cart = request.session.get('cart')
        remove = request.POST.get('remove')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = 1 + quantity
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print(request.session.get('cart'))

        return redirect('homepage')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email,
            'password':password
        }
        error_message = None

        customer = Customer(first_name=first_name, last_name=last_name, phone=phone, email=email, password=password)


        if (not customer.first_name):
            error_message = "First Name Required !!"
        elif len(customer.first_name) < 4:
            error_message = 'First Name must be 4 char long or more'
        elif not customer.last_name:
            error_message = 'Last Name Required'
        elif len(customer.last_name) < 4:
            error_message = 'Last Name must be 4 char long or more'
        elif not customer.phone:
            error_message = 'Phone Number required'
        elif len(customer.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len(customer.password) < 6:
            error_message = 'Password must be 6 char long'
        elif len(customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif customer.isExists():
            error_message = 'Email Address Already Registered..'



        if not error_message:
            print(first_name, last_name, phone, email, password)
            # hashing password
            customer.password = make_password(customer.password)
            #saving details in customre model
            customer.register()
            return redirect('homepage')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)


class LoginView(View):
    return_url = None
    def get(self, request):
        LoginView.return_url = request.GET.get('return_url')
        return render(request, 'login.html')
    
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            customer = Customer.objects.get(email = email)
        except:
            error_message = 'Email or Password is invalid'
            return render(request, 'login.html', {'error':error_message})
        print(customer)

        if customer:
           
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                request.session['email'] = customer.email
                if LoginView.return_url:
                    return HttpResponseRedirect(LoginView.return_url)
                else:
                    LoginView.return_url = None
                    return redirect('homepage')
            else:
                error_message = 'Email or Password is invalid'

        else:
            error_message = 'Email or Password is invalid'
        return render(request, 'login.html', {'error':error_message})


def logout(request):
    request.session.clear()
    return redirect('/login')


class cartView(View):
    def get(self, request):
        if not request.session.get('cart'):
           request.session['cart'] = {}
        
        ids = list(request.session.get('cart').keys())
        products = Product.get_product_by_ids(ids)
        return render(request, 'cart.html', {'products':products})


class checkoutView(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_product_by_ids(list(cart.keys()))
        # print(address, phone, customer, cart, products)
        print("CUSTOMRE ::::::::::::",customer)
        for product in products:
            order = Order(customer=Customer(id=customer),
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))
            if customer is not None:
                order.save()
            else:
                return redirect('loginpage')
        request.session['cart'] = {}

        return redirect('/cart')


class orderView(View):

    # @method_decorator(auth_middleware)
    def get(self , request ):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        return render(request , 'orders.html'  , {'orders' : orders})




