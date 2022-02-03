from django.forms import formsets, modelformset_factory
from django.contrib.auth.models import User, auth
from django.http import request, FileResponse
# ----For PDF Create----
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from unagaapp.models import Transfer
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
# from passlib.hash import pbkdf2_sha256
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render
import os

import pickle
from.models import Arrivals, Banner, Category, Damaged_list, Order, Product, Right_Banner, Sub_Category, Unaga_user, Left_Banner, Wardrobe, Customer_Register, Customer_Contact, Add_To_Cart,checkout
from.forms import Category_Form, Damages_Form, Order_Form, Sub_Category_Form, Transfer_Form, Wardrobe_Form


# Create your views here.

# def index(request):
#     employees = Personal_details.objects.all()
#     stocks = Stocks.objects.all()
#     employees_count = employees.count()
#     stocks_count = stocks.count()
#     context = {
#         'employees': employees,
#         'employees_count': employees_count,
#         'stocks': stocks,
#         'stocks_count': stocks_count
#     }
#     return render(request, "index.html", context)


def index(request):
    orders = Order.objects.all()
    products = Product.objects.all()
    users = Customer_Register.objects.all()
    orders_count = orders.count()
    products_count = products.count()
    users_count = users.count()
    context = {
        'orders': orders,
        'products': products,
        'users': users,
        'orders_count': orders_count,
        'products_count': products_count,
        'users_count': users_count,
        'username': getUserDetails("data.pickle")
    }
    return render(request, 'index.html', context)


# def login(request):
#     return render(request, 'login.html')
# -----------------------------------------------------------------------------------------------------------------

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # enc_password = pbkdf2_sha256.encrypt(
        #     password, rounds=12000, salt_size=32)
        # enc_password = make_password(password)

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken already')
                return redirect('/register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken already')
                return redirect('/register')
            else:
                myuser = User.objects.create(username=username,
                                             email=email, password=password)
                myuser.user_name = username
                myuser.save()
                messages.info(request, 'User created successfully!...')
                return redirect('/login')
        else:
            messages.info(request, 'Password not matching')
            return redirect('/register')
    else:
        return render(request, 'register.html')


# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']

#         user = authenticate(username=username, password=password)

#         if user is None:
#             login(request, user)
#             username = user.user_name
#             return render(request, 'index.html', {'username': username})

#         else:
#             messages.success(request, 'Username / Password Invalid...!')
#             return render(request, 'index.html')
#     return render(request, 'login.html')


# ----------------------------------------------------------------------------------------------------------------


# def register(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']
#         confirm_password = request.POST['confirm_password']

#         if password == confirm_password:
#             if Register.objects.filter(username=username).exists():
#                 messages.info(request, 'Username Taken already')
#                 return redirect('/register')
#             elif Register.objects.filter(email=email).exists():
#                 messages.info(request, 'Email Taken already')
#                 return redirect('/register')
#             else:
#                 Register(username=username, email=email, password=password,
#                          confirm_password=confirm_password).save()
#                 return redirect('/login')
#         else:
#             messages.info(request, 'Password not matching')
#             return redirect('/register')
#     else:
#         return render(request, 'register.html')
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
def setUserDetails(obj):
    try:
        with open("data.pickle", "wb") as f:
            pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as ex:
        print("Error during pickling object (Possibly unsupported):", ex)


def getUserDetails(filename):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except Exception as ex:
        print("Error during unpickling object (Possibly unsupported):", ex)


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def login(request):
    orders = Order.objects.all()
    products = Product.objects.all()
    users = Customer_Register.objects.all()
    orders_count = orders.count()
    products_count = products.count()
    users_count = users.count()
    context = {
        'orders': orders,
        'products': products,
        'users': users,
        'orders_count': orders_count,
        'products_count': products_count,
        'users_count': users_count
    }
    if request.method == "POST":
        try:
            Userdetails = User.objects.get(
                username=request.POST['username'], password=request.POST['password'])
            context['username'] = Userdetails
            setUserDetails(Userdetails)
            request.session['username'] = Userdetails.username
            return render(request, 'index.html', context)
        except User.DoesNotExist as e:
            messages.success(request, 'Username / Password Invalid...!')
    return render(request, 'login.html')


def logout(request):
    try:
        del request.session['email']
    except:
        return render(request, 'login.html')
    return render(request, 'login.html')


# def user_list(request):
#     users = User.objects.all()
#     return render(request, 'users-list.html', {'users': users})


def dashboard(request):
    orders = Order.objects.all()
    products = Product.objects.all()
    users = Customer_Register.objects.all()
    # Userdetails = User.objects.username()
    orders_count = orders.count()
    products_count = products.count()
    users_count = users.count()
    context = {
        'orders': orders,
        'products': products,
        'users': users,
        'orders_count': orders_count,
        'products_count': products_count,
        'users_count': users_count,
        'username': getUserDetails("data.pickle")
    }
    return render(request, 'index.html', context)

# ------------------------------------------------------------------------------------------------------------------------------------------------

# category part


def add_category(request):
    sub_category = Sub_Category.objects.all()
    if request.method == 'POST':
        form = Category_Form(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, ' Category added successfully')
            except:
                pass
    else:
        form = Category_Form()
    return render(request, 'add-category.html', {'form': form, 'sub_category': sub_category, 'username': getUserDetails("data.pickle")})


def view_category(request):
    categories = Category.objects.all()
    return render(request, 'view-category.html', {'categories': categories, 'username': getUserDetails("data.pickle")})


def edit_category(request, id):
    sub_category = Sub_Category.objects.all()
    category = Category.objects.get(id=id)
    return render(request, 'edit-category.html', {'category': category, 'sub_category': sub_category})


def update_category(request, id):
    sub_category = Sub_Category.objects.all()
    category = Category.objects.get(id=id)
    form = Category_Form(request.POST, instance=category)
    if form.is_valid():
        form.save()
        messages.success(request, ' Category updated successfully')
        return redirect("/view_category")
    return render(request, 'edit-category.html', {'category': category, 'sub_category': sub_category})


def delete_category(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    messages.success(request, ' Deleted successfully')
    return redirect("/view_category")


# ---------------------------------------------------------------------------------------------------------------------------------
# sub category part

def add_sub_category(request):
    category = Category.objects.all()
    if request.method == 'POST':
        form = Sub_Category_Form(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, ' Sub-Category added successfully')
            except:
                pass
    else:
        form = Sub_Category_Form()
    return render(request, 'add-sub-category.html', {'form': form, 'category': category})


def view_sub_category(request):
    sub_categories = Sub_Category.objects.all()
    return render(request, 'view-sub-category.html', {'sub_categories': sub_categories})


def edit_sub_category(request, id):
    category = Category.objects.all()
    sub_category = Sub_Category.objects.get(id=id)
    return render(request, 'edit-sub-category.html', {'sub_category': sub_category, 'category': category})


def update_sub_category(request, id):
    category = Category.objects.all()
    sub_category = Sub_Category.objects.get(id=id)
    form = Sub_Category_Form(request.POST, instance=sub_category)
    if form.is_valid():
        form.save()
        messages.success(request, ' Sub_Category updated successfully')
        return redirect("/view_sub_category")
    return render(request, 'edit-sub-category.html', {'sub_category': sub_category, 'category': category})


def delete_sub_category(request, id):
    sub_category = Sub_Category.objects.get(id=id)
    sub_category.delete()
    messages.success(request, ' Deleted successfully')
    return redirect("/view_sub_category")

# --------------------------------------------------------------------------------------------------------------------------------------------------

# product part


# def add_product(request):
#     category = Category.objects.all()
#     sub_category = Sub_Category.objects.all()

#     if request.method == "POST":
#         product = Product()
#         product.product_name = request.POST.get("product_name")
#         product.product_code = request.POST.get("product_code")
#         product.description = request.POST.get("description")
#         product.categories = request.POST.get("categories")
#         product.sub_categories = request.POST.get("sub_categories")
#         product.brands = request.POST.get("brands")
#         product.variant_color = request.POST.get("variant_color")
#         product.sizes = request.POST.get("sizes")
#         product.unit_price = request.POST.get("unit_price")
#         product.purchase_price = request.POST.get("purchase_price")
#         product.tax = request.POST.get("tax")
#         product.gst = request.POST.get("gst")
#         product.discount = request.POST.get("discount")
#         product.total_quantity = request.POST.get("total_quantity")
#         product.meta_title = request.POST.get("meta_title")
#         product.meta_description = request.POST.get("meta_description")

#         if len(request.FILES) != 0:
#             product.image1 = request.FILES['image1']

#         if len(request.FILES) != 0:
#             product.image2 = request.FILES['image2']

#         if len(request.FILES) != 0:
#             product.image3 = request.FILES['image3']

#         if len(request.FILES) != 0:
#             product.image4 = request.FILES['image4']

#         product.save()
#         messages.success(request, ' Product added successfully')
#     return render(request, 'add-product.html', {'category': category, 'sub_category': sub_category})

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

def add_product(request):
    main_category = Category.objects.all()
    sub_category = Sub_Category.objects.all()

    if request.method == "POST":
        product_name = request.POST.get("product_name")
        product_code = request.POST.get("product_code")
        description = request.POST.get("description")
        categories = request.POST.get("categories")
        sub_categories = request.POST.get("sub_categories")
        # brands = request.POST.get("brands")
        fabric = request.POST.get("fabric")
        work = request.POST.get("work")
        fabric_care = request.POST.get("fabric_care")
        variant_color = ",".join([i for i in request.POST.getlist("variant_color")])
        sizes = ",".join([j for j in request.POST.getlist("sizes")])
        unit_price = request.POST.get("unit_price")
        purchase_price = request.POST.get("purchase_price")
        tax = request.POST.get("tax")
        gst = request.POST.get("gst")
        discount = request.POST.get("discount")
        total_quantity = request.POST.get("total_quantity")
        meta_title = request.POST.get("meta_title")
        meta_description = request.POST.get("meta_description")

        if len(request.FILES) != 0:
            image1 = request.FILES['image1']
        if len(request.FILES) != 0:
            image2 = request.FILES['image2']

        if len(request.FILES) != 0:
            image3 = request.FILES['image3']
        if len(request.FILES) != 0:
            image4 = request.FILES['image4']
        #for c in variant_color:
            prod = Product(product_name=product_name, product_code=product_code, description=description, categories=categories,
                       sub_categories=sub_categories, fabric=fabric, work=work, fabric_care=fabric_care, variant_color=variant_color, sizes=sizes, unit_price=unit_price, purchase_price=purchase_price, tax=tax, gst=gst, discount=discount, total_quantity=total_quantity,
                       meta_title=meta_title, meta_description=meta_description, image1=image1,
                       image2=image2, image3=image3, image4=image4)
        prod.save()
        messages.success(request, ' Product added successfully')
        return redirect("/add_product")


    return render(request, 'add-product.html', {'main_category': main_category, 'sub_category': sub_category})


def view_product(request):
    products = Product.objects.all()
    orders = Order.objects.all()
    return render(request, 'view-product.html', {'products': products, 'orders': orders})


def edit_product(request, id):
    category = Category.objects.all()
    sub_category = Sub_Category.objects.all()
    product = Product.objects.get(id=id)
    if request.method == "POST":
        product.product_name = request.POST.get("product_name")
        product.product_code = request.POST.get("product_code")
        product.description = request.POST.get("description")
        product.categories = request.POST.get("categories")
        product.sub_categories = request.POST.get("sub_categories")
        if not request.POST.getlist("variant_color[]") == []:
            product.variant_color = ",".join([ i for i in request.POST.getlist("variant_color[]")])

        if not request.POST.getlist("sizes[]") == []:
            product.sizes = ",".join([j for j in request.POST.getlist("sizes[]")])
        # product.brands = request.POST.get("brands")
        product.fabric = request.POST.get("fabric")
        product.work = request.POST.get("work")
        product.fabric_care = request.POST.get("fabric_care")
        # product.variant_color = request.POST.get("variant_color")
        # product.sizes = request.POST.getlist("sizes")
        product.unit_price = request.POST.get("unit_price")
        product.purchase_price = request.POST.get("purchase_price")
        product.tax = request.POST.get("tax")
        product.gst = request.POST.get("gst")
        product.discount = request.POST.get("discount")
        product.total_quantity = request.POST.get("total_quantity")
        product.meta_title = request.POST.get("meta_title")
        product.meta_description = request.POST.get("meta_description")
        if len(request.FILES) != 0:
            try:
                product.image1 = request.FILES['image1']
            except:
                pass

        if len(request.FILES) != 0:
            try:
                product.image2 = request.FILES['image2']
            except:
                pass

        if len(request.FILES) != 0:
            try:
                product.image3 = request.FILES['image3']
            except:
                pass

        if len(request.FILES) != 0:
            try:
                product.image4 = request.FILES['image4']
            except:
                pass
        product.save()
        messages.success(request, ' Product updated successfully')
        return redirect("/view_product")
    product = Product.objects.filter(id=id)
    context = {'product': product, 'category': category,
               "sub_category": sub_category}
    return render(request, 'edit-product.html', context)


def delete_product(request, id):
    product = Product.objects.get(id=id)
    if len(product.image1) > 0:
        os.remove(product.image1.path)

    if len(product.image2) > 0:
        os.remove(product.image2.path)

    if len(product.image3) > 0:
        os.remove(product.image3.path)

    if len(product.image4) > 0:
        os.remove(product.image4.path)
    product.delete()
    messages.success(request, ' Deleted successfully')
    return redirect("/view_product")

# def delete_product(request, id):
#     product = Product.objects.get(id=id)
#     product.delete()
#     return redirect("/view_product")


# ----------------------------------------------------------------------------------------------------------------------------------------------------

# order part


# def add_order(request):
#     if request.method == 'POST':
#         form = Order_Form(request.POST)
#         if form.is_valid():
#             try:
#                 form.save()
#                 messages.success(request, ' Order added successfully')
#             except:
#                 pass
#     else:
#         form = Order_Form()
#     return render(request, 'add-order.html', {'form': form})

def add_order(request):
    if request.method == "POST":
        order = Order()
        order.customer_name = request.POST.get("customer_name")
        order.mobile_no = request.POST.get("mobile_no")
        order.product_name = request.POST.get("product_name")
        order.product_code = request.POST.get("product_code")
        order.ref_no = request.POST.get("ref_no")
        order.created_on = request.POST.get("created_on")
        order.save()
        messages.success(request, ' Order added successfully')
    return render(request, 'add-order.html')


def manage_order(request):
    orders = Order.objects.all()
    products = Product.objects.all()
    return render(request, 'manage-order.html', {'orders': orders, 'products': products})


def edit_order(request, id):
    order = Order.objects.get(id=id)
    if request.method == "POST":
        order.customer_name = request.POST.get("customer_name")
        order.mobile_no = request.POST.get("mobile_no")
        order.product_name = request.POST.get("product_name")
        order.product_code = request.POST.get("product_code")
        order.ref_no = request.POST.get("ref_no")
        order.created_on = request.POST.get("created_on")
        order.save()
        messages.success(request, ' Order updated successfully')
        return redirect("/manage_order")
    context = {"order": order}
    return render(request, "edit-order.html", context)


# def edit_order(request, id):
#     order = Order.objects.get(id=id)
#     return render(request, 'edit-order.html', {'order': order})


# def update_order(request, id):
#     order = Order.objects.get(id=id)
#     form = Order_Form(request.POST, instance=order)
#     if form.is_valid():
#         form.save()
#         return redirect("/manage_order")
#     return render(request, "edit-order.html", {'order': order})


def delete_order(request, id):
    order = Order.objects.get(id=id)
    order.delete()
    messages.success(request, ' Deleted successfully')
    return redirect("/manage_order")


# -----------------------------------------------------------------------------------------------------------------------------------------------------

# inventory part


# def add_inventory(request):
#     category = Category.objects.all()
#     sub_category = Sub_Category.objects.all()
#     if request.method == 'POST':
#         form = Inventory_Form(request.POST)
#         if form.is_valid():
#             try:
#                 form.save()
#                 messages.success(request, ' Inventory added successfully')
#             except:
#                 pass
#     else:
#         form = Inventory_Form()
#     return render(request, 'add-inventory.html', {'form': form, "category": category, "sub_category": sub_category})


def manage_inventory(request):
    products = Product.objects.all()
    return render(request, 'manage-inventory.html', {'products': products})


def edit_inventory(request, id):
    category = Category.objects.all()
    sub_category = Sub_Category.objects.all()
    product = Product.objects.get(id=id)
    if request.method == "POST":
        product.product_name = request.POST.get("product_name")
        product.product_code = request.POST.get("product_code")
        product.description = request.POST.get("description")
        product.categories = request.POST.get("categories")
        product.sub_categories = request.POST.get("sub_categories")
        product.brands = request.POST.get("brands")
        product.variant_color = request.POST.get("variant_color")
        product.sizes = request.POST.get("sizes")
        product.unit_price = request.POST.get("unit_price")
        product.purchase_price = request.POST.get("purchase_price")
        product.tax = request.POST.get("tax")
        product.gst = request.POST.get("gst")
        product.discount = request.POST.get("discount")
        product.total_quantity = request.POST.get("total_quantity")
        product.add_qty = request.POST.get("add_qty")
        total = int(product.total_quantity) + int(product.add_qty)
        product.meta_title = request.POST.get("meta_title")
        product.meta_description = request.POST.get("meta_description")
        if len(request.FILES) != 0:
            try:
                product.image1 = request.FILES['image1']
            except:
                pass

        if len(request.FILES) != 0:
            try:
                product.image2 = request.FILES['image2']
            except:
                pass

        if len(request.FILES) != 0:
            try:
                product.image3 = request.FILES['image3']
            except:
                pass

        if len(request.FILES) != 0:
            try:
                product.image4 = request.FILES['image4']
            except:
                pass
        product.save()
        messages.success(request, ' Inventory updated successfully')
        return redirect("/manage_inventory")
    context = {'product': product, 'category': category,
               "sub_category": sub_category}
    return render(request, 'edit-inventory.html', context)


# def edit_inventory(request, id):
#     inventory = Inventory.objects.get(id=id)
#     return render(request, 'edit-inventory.html', {'inventory': inventory})


# def update_inventory(request, id):
#     inventory = Inventory.objects.get(id=id)
#     form = Inventory_Form(request.POST, instance=inventory)
#     if form.is_valid():
#         form.save()
#         return redirect("/manage_inventory")
#     return render(request, 'edit-inventory.html', {"inventory": inventory})


# def delete_inventory(request, id):
#     inventory = Inventory.objects.get(id=id)
#     inventory.delete()
#     return redirect("/manage_inventory")

# ------------------------------------------------------------------------------------------------------------------------------------------------------

# damages part
# def add_damaged_list(request, id):
#     product = Product.objects.get(id=id)
#     context = {"product": product}
#     if request.method == "POST":
#         damaged = Damaged_list()
#         damaged.product_name = request.POST.get("product_name")
#         damaged.product_code = request.POST.get("product_code")
#         damaged.categories = request.POST.get("categories")
#         damaged.sub_categories = request.POST.get("sub_categories")
#         damaged.unit_price = request.POST.get("unit_price")
#         damaged.purchase_price = request.POST.get("purchase_price")
#         damaged.total_quantity = request.POST.get("total_quantity")
#         damaged.damaged_quantity = request.POST.get("damaged_quantity")
#         a = int(damaged.total_quantity)-int(damaged.damaged_quantity)
#         damaged.save()
#         messages.success(request, ' Damaged added successfully')
#     return render(request, 'add-damaged-list.html', context)

    # -------------------------------------------------------------------------------------

def add_damaged_list(request, id):
    product = Product.objects.get(id=id)
    context = {"product": product}
    if request.method == "POST":

        pId = (request.POST.get("pId"))
        dmg = int(request.POST.get("damaged_quantity"))

        if Product.objects.filter(product_code=pId):
            if Damaged_list.objects.filter(product_code=pId):
                a = Damaged_list.objects.get(product_code=pId)
                product.total_quantity = int(product.total_quantity)-dmg
                product.save()
                a.total_quantity = int(a.total_quantity) - dmg
                a.damaged_quantity = int(a.damaged_quantity) + dmg
                a.save()
                messages.success(request, ' Damaged added successfully')
            else:
                a = Damaged_list()
                a.product_name = product.product_name
                a.product_code = product.product_code
                a.categories = product.categories
                a.sub_categories = product.sub_categories
                a.unit_price = product.unit_price
                a.purchase_price = (product.purchase_price)
                total = int(product.total_quantity)-dmg
                product.total_quantity = total
                product.save()
                a.total_quantity = total

                # print(product.damaged_quantity)
                a.damaged_quantity = dmg
                a.save()
                messages.info(request, "Add damaged successfully")

        else:
            messages.error(request, 'Invalid Product Id')

        return redirect(f'/add_damaged_list/{id}')

    return render(request, 'add-damaged-list.html', context)

    # ------------------------------------------------------------------------------------


def view_damaged_list(request):
    damages = Damaged_list.objects.all()
    return render(request, 'view-damaged-list.html', {'damages': damages})


def edit_damaged_list(request, id):
    damaged = Damaged_list.objects.get(id=id)
    if request.method == "POST":
        damaged.product_name = request.POST.get("product_name")
        damaged.product_code = request.POST.get("product_code")
        damaged.categories = request.POST.get("categories")
        damaged.sub_categories = request.POST.get("sub_categories")
        damaged.unit_price = request.POST.get("unit_price")
        damaged.purchase_price = request.POST.get("purchase_price")
        damaged.total_quantity = request.POST.get("total_quantity")
        damaged.damaged_quantity = request.POST.get("damaged_quantity")
        damaged.save()
        messages.success(request, ' Damages updated successfully')
        return redirect("/view_damaged_list")
    context = {"damaged": damaged}
    return render(request, "edit-damaged-list.html", context)


# def add_damaged_list(request, id):
#     product = Product.objects.get(id=id)
#     if request.method == 'POST':
#         form = Damages_Form(request.POST)
#         if form.is_valid():
#             try:
#                 form.save()
#                 messages.success(request, ' Damages added successfully')
#             except:
#                 pass
#     else:
#         form = Damages_Form()
#     return render(request, 'add-damaged-list.html', {'form': form, 'product': product})


# def view_damaged_list(request):
#     damages = Damaged_list.objects.all()
#     return render(request, 'view-damaged-list.html', {'damages': damages})


# def edit_damaged_list(request, id):
#     product = Product.objects.get(id=id)
#     damaged = Damaged_list.objects.get(id=id)
#     return render(request, 'edit-damaged-list.html', {'damaged': damaged, 'product': product})


# def update_damaged_list(request, id):
#     product = Product.objects.get(id=id)
#     damaged = Damaged_list.objects.get(id=id)
#     form = Damages_Form(request.POST, instance=damaged)
#     if form.is_valid():
#         form.save()
#         return redirect("/view_damaged_list")
#     return render(request, "edit-damaged-list.html", {'damaged': damaged, 'product': product})


def delete_damaged_list(request, id):
    damaged = Damaged_list.objects.get(id=id)
    damaged.delete()
    messages.success(request, ' Deleted successfully')
    return redirect("/view_damaged_list", {'damaged': damaged})


# ------------------------------------------------------------------------------------------------------------------------------------------------------

# transfer part


def add_transfer(request):
    category = Category.objects.all()
    sub_category = Sub_Category.objects.all()
    product = Product.objects.all()

    if request.method == "POST":
        transfer = Transfer()
        transfer.date = request.POST.get("date")
        transfer.product_name = request.POST.get("product_name")
        transfer.categories = request.POST.get("categories")
        transfer.sub_categories = request.POST.get("sub_categories")
        transfer.select_branch1 = request.POST.get("select_branch1")
        transfer.quantity = request.POST.get("quantity")
        transfer.select_branch2 = request.POST.get("select_branch2")
        transfer.save()
        messages.success(request, ' Transfer added successfully')
    return render(request, 'add-transfer.html', {'category': category, 'sub_category': sub_category, 'product': product})


def manage_transfer(request):
    transfers = Transfer.objects.all()
    return render(request, 'manage-transfer.html', {"transfers": transfers})


def delete_transfer(request, id):
    transfer = Transfer.objects.get(id=id)
    transfer.delete()
    messages.success(request, ' Deleted successfully')
    return redirect("/manage_transfer")


# ------------------------------------------------------------------------------------------------------------------------------------------------------
# banners part
def add_banner(request):
    if request.method == "POST":
        banner = Banner()
        banner.banner_name = request.POST.get("banner_name")
        if len(request.FILES) != 0:
            banner.banner_image1 = request.FILES['banner_image1']
        if len(request.FILES) != 0:
            banner.banner_image2 = request.FILES['banner_image2']
        if len(request.FILES) != 0:
            banner.banner_image3 = request.FILES['banner_image3']
        if len(request.FILES) != 0:
            banner.banner_image4 = request.FILES['banner_image4']
        if len(request.FILES) != 0:
            banner.banner_image5 = request.FILES['banner_image5']
        banner.banner_content = request.POST.get("banner_content")
        banner.banner_url = request.POST.get("banner_url")
        banner.save()
        messages.success(request, ' Banner added successfully')
    return render(request, "add-banner.html")


def view_banner(request):
    banners = Banner.objects.all()
    return render(request, "view-banner.html", {'banners': banners})


def edit_banner(request, id):
    banner = Banner.objects.get(id=id)
    if request.method == "POST":
        banner.banner_name = request.POST.get("banner_name")
        if len(request.FILES) != 0:
            try:
                banner.banner_image1 = request.FILES['banner_image1']
            except:
                pass
        if len(request.FILES) != 0:
            try:
                banner.banner_image2 = request.FILES['banner_image2']
            except:
                pass
        if len(request.FILES) != 0:
            try:
                banner.banner_image3 = request.FILES['banner_image3']
            except:
                pass
        if len(request.FILES) != 0:
            try:
                banner.banner_image4 = request.FILES['banner_image4']
            except:
                pass
        if len(request.FILES) != 0:
            try:
                banner.banner_image5 = request.FILES['banner_image5']
            except:
                pass
        banner.banner_content = request.POST.get("banner_content")
        banner.banner_url = request.POST.get("banner_url")
        banner.save()
        messages.success(request, ' banner updated successfully')
        return redirect("/view_banner")
    context = {"banner": banner}
    return render(request, "edit-banner.html", context)


def delete_banner(request, id):
    banner = Banner.objects.get(id=id)
    if len(banner.banner_image1) > 0:
        os.remove(banner.banner_image1.path)
    if len(banner.banner_image2) > 0:
        os.remove(banner.banner_image2.path)
    if len(banner.banner_image3) > 0:
        os.remove(banner.banner_image3.path)
    if len(banner.banner_image4) > 0:
        os.remove(banner.banner_image4.path)
    if len(banner.banner_image5) > 0:
        os.remove(banner.banner_image5.path)
    banner.delete()
    messages.success(request, ' Deleted successfully')
    return redirect("/view_banner")

# -------------------------------------------------------------------------------------------------------------------------------------------------
# left banner


def add_leftbanner(request):
    if request.method == "POST":
        leftbanner = Left_Banner()
        leftbanner.leftbanner_name = request.POST.get("leftbanner_name")
        if len(request.FILES) != 0:
            leftbanner.leftbanner_image1 = request.FILES['leftbanner_image1']
        if len(request.FILES) != 0:
            leftbanner.leftbanner_image2 = request.FILES['leftbanner_image2']
        leftbanner.leftbanner_content = request.POST.get("leftbanner_content")
        leftbanner.leftbanner_url = request.POST.get("leftbanner_url")
        leftbanner.save()
        messages.success(request, ' LeftBanner added successfully')
    return render(request, "add-leftbanner.html")


def view_leftbanner(request):
    leftbanners = Left_Banner.objects.all()
    return render(request, "view-leftbanner.html", {'leftbanners': leftbanners})


def edit_leftbanner(request, id):
    leftbanner = Left_Banner.objects.get(id=id)
    if request.method == "POST":
        leftbanner.leftbanner_name = request.POST.get("leftbanner_name")
        if len(request.FILES) != 0:
            try:
                leftbanner.leftbanner_image1 = request.FILES['leftbanner_image1']
            except:
                pass
        if len(request.FILES) != 0:
            try:
                leftbanner.leftbanner_image2 = request.FILES['leftbanner_image2']
            except:
                pass
        leftbanner.leftbanner_content = request.POST.get("leftbanner_content")
        leftbanner.leftbanner_url = request.POST.get("leftbanner_url")
        leftbanner.save()
        messages.success(request, ' left-banner updated successfully')
        return redirect("/view_leftbanner")
    context = {"leftbanner": leftbanner}
    return render(request, "edit-leftbanner.html", context)


def delete_leftbanner(request, id):
    leftbanner = Left_Banner.objects.get(id=id)
    if len(leftbanner.leftbanner_image1) > 0:
        os.remove(leftbanner.leftbanner_image1.path)
    if len(leftbanner.leftbanner_image2) > 0:
        os.remove(leftbanner.leftbanner_image2.path)
    leftbanner.delete()
    messages.success(request, ' Deleted successfully')
    return redirect("/view_leftbanner")

# -------------------------------------------------------------------------------------------------------------------------------------------------------
# right-banner part


def add_rightbanner(request):
    if request.method == "POST":
        rightbanner = Right_Banner()
        rightbanner.rightbanner_name = request.POST.get("rightbanner_name")
        if len(request.FILES) != 0:
            rightbanner.rightbanner_image1 = request.FILES['rightbanner_image1']
        if len(request.FILES) != 0:
            rightbanner.rightbanner_image2 = request.FILES['rightbanner_image2']
        rightbanner.rightbanner_content = request.POST.get(
            "rightbanner_content")
        rightbanner.rightbanner_url = request.POST.get("rightbanner_url")
        rightbanner.save()
        messages.success(request, ' RightBanner added successfully')
    return render(request, "add-rightbanner.html")


def view_rightbanner(request):
    rightbanners = Right_Banner.objects.all()
    return render(request, "view-rightbanner.html", {'rightbanners': rightbanners})


def edit_rightbanner(request, id):
    rightbanner = Right_Banner.objects.get(id=id)
    if request.method == "POST":
        rightbanner.rightbanner_name = request.POST.get("rightbanner_name")
        if len(request.FILES) != 0:
            try:
                rightbanner.rightbanner_image1 = request.FILES['rightbanner_image1']
            except:
                pass
        if len(request.FILES) != 0:
            try:
                rightbanner.rightbanner_image2 = request.FILES['rightbanner_image2']
            except:
                pass
        rightbanner.rightbanner_content = request.POST.get(
            "rightbanner_content")
        rightbanner.rightbanner_url = request.POST.get("rightbanner_url")
        rightbanner.save()
        messages.success(request, ' right-banner updated successfully')
        return redirect("/view_rightbanner")
    context = {"rightbanner": rightbanner}
    return render(request, "edit-rightbanner.html", context)


def delete_rightbanner(request, id):
    rightbanner = Right_Banner.objects.get(id=id)
    if len(rightbanner.rightbanner_image1) > 0:
        os.remove(rightbanner.rightbanner_image1.path)
    if len(rightbanner.rightbanner_image2) > 0:
        os.remove(rightbanner.rightbanner_image2.path)
    rightbanner.delete()
    messages.success(request, ' Deleted successfully')
    return redirect("/view_rightbanner")

# -------------------------------------------------------------------------------------------------------------------------------------------------------
# cuatomer part


# def add_customer(request):
#     if request.method == 'POST':
#         customer = Customer()
#         customer.customer_name = request.POST.get("customer_name")
#         customer.customer_mobile = request.POST.get("customer_mobile")
#         customer.customer_email = request.POST.get("customer_email")
#         customer.customer_address = request.POST.get("customer_address")
#         customer.customer_username = request.POST.get("customer_username")
#         customer.customer_password = request.POST.get("customer_password")
#         customer.save()
#         messages.success(request, ' Customer added successfully')
#     return render(request, 'add-customer.html')


# def view_customer(request):
#     customers = Customer.objects.all()
#     return render(request, 'customer-list.html', {'customers': customers})


# def edit_customer(request, id):
#     customer = Customer.objects.get(id=id)
#     if request.method == 'POST':
#         customer.customer_name = request.POST.get("customer_name")
#         customer.customer_mobile = request.POST.get("customer_mobile")
#         customer.customer_email = request.POST.get("customer_email")
#         customer.customer_address = request.POST.get("customer_address")
#         customer.customer_username = request.POST.get("customer_username")
#         customer.customer_password = request.POST.get("customer_password")
#         customer.save()
#         messages.success(request, ' Customer Updated successfully')
#         return redirect("/view_customer")
#     context = {"customer": customer}
#     return render(request, 'edit-customer.html', context)


# def delete_customer(request, id):
#     customer = Customer.objects.get(id=id)
#     customer.delete()
#     messages.success(request, ' Customer deleted successfully')
#     return redirect("/view_customer")


# -------------------------------------------------------------------------------------------------------------------------------------------------------
# user part

def add_user(request):
    if request.method == 'POST':
        user = Unaga_user()
        user.user_name = request.POST.get("user_name")
        user.user_mobile = request.POST.get("user_mobile")
        user.user_username = request.POST.get("user_username")
        user.user_password = request.POST.get("user_password")
        user.save()
        messages.success(request, ' User added successfully')
    return render(request, 'add-user.html')


def view_user(request):
    users = Unaga_user.objects.all()
    return render(request, 'user-list.html', {'users': users})


def edit_user(request, id):
    user = Unaga_user.objects.get(id=id)
    if request.method == 'POST':
        user.user_name = request.POST.get("user_name")
        user.user_mobile = request.POST.get("user_mobile")
        user.user_username = request.POST.get("user_username")
        user.user_password = request.POST.get("user_password")
        user.save()
        messages.success(request, ' User Updated successfully')
        return redirect("/view_user")
    context = {"user": user}
    return render(request, 'edit-user.html', context)


def delete_user(request, id):
    user = Unaga_user.objects.get(id=id)
    user.delete()
    messages.success(request, ' User deleted successfully')
    return redirect("/view_user")
# ---------------------------------------------------------------------------------------------------------------------------------
# wardrobe part


def add_wardrobe(request):
    if request.method == "POST":
        wardrobe = Wardrobe()
        wardrobe.customer_name = request.POST.get("customer_name")
        wardrobe.mobile_no = request.POST.get("mobile_no")
        wardrobe.alt_mobile = request.POST.get("alt_mobile")
        wardrobe.email_id = request.POST.get("email_id")
        wardrobe.no_dressess = request.POST.get("no_dressess")
        if len(request.FILES) != 0:
            wardrobe.images = request.FILES.getlist('images')
        wardrobe.date = request.POST.get("date")
        wardrobe.time = request.POST.get("time")
        wardrobe.wardrobe_no = request.POST.get("wardrobe_no")
        wardrobe.reciever_name = request.POST.get("reciever_name")
        for f in wardrobe.images:
            Wardrobe(images=f, customer_name=wardrobe.customer_name, mobile_no=wardrobe.mobile_no,
                     alt_mobile=wardrobe.alt_mobile, email_id=wardrobe.email_id, no_dressess=wardrobe.no_dressess, date=wardrobe.date, time=wardrobe.time, wardrobe_no=wardrobe.wardrobe_no, reciever_name=wardrobe.reciever_name).save()
        messages.success(request, ' Wardrobe added successfully')
        # wardrobe.save()
        # messages.success(request, ' Wardrobe added successfully')
    return render(request, "add-wardrobe.html")

# def add_wardrobe(request):
#     if request.method == "POST":
#         form = Wardrobe_Form(request.POST, request.FILES)
#         files = request.FILES.getlist('images')
#         if form.is_valid():
#             for f in files:
#                 file_instance = Wardrobe(images=f)
#                 file_instance.save()
#                 messages.success(request, ' Wardrobe added successfully')
#         else:
#             form = Wardrobe_Form()
#     return render(request, "add-wardrobe.html")


def view_wardrobe(request):
    wardrobes = Wardrobe.objects.all()
    return render(request, 'view-wardrobe.html', {"wardrobes": wardrobes})


def delete_wardrobe(request, id):
    wardrobe = Wardrobe.objects.get(id=id)
    wardrobe.delete()
    messages.success(request, ' Wardrobe deleted successfully')
    return redirect("/view_wardrobe")

# --------------------------------------------------------------------------------------------------------------------------------
# Arrivals part


def add_arrivals(request):
    if request.method == "POST":
        arrivals = Arrivals()
        if len(request.FILES) != 0:
            arrivals.arrival_img = request.FILES['arrival_img']
        arrivals.arrival_content = request.POST.get(
            "arrival_content")
        arrivals.arrival_date = request.POST.get("arrival_date")
        arrivals.save()
        messages.success(request, ' product added successfully')
    return render(request, 'add-latest-arrivals.html')


def view_arrivals(request):
    arrivals = Arrivals.objects.all()
    return render(request, 'view-latest-arrivals.html', {"arrivals": arrivals})


def edit_arrivals(request, id):
    arrival = Arrivals.objects.get(id=id)
    if request.method == "POST":
        if len(request.FILES) != 0:
            arrival.arrival_img = request.FILES['arrival_img']
        arrival.arrival_content = request.POST.get(
            "arrival_content")
        arrival.arrival_date = request.POST.get("arrival_date")
        arrival.save()
        messages.success(request, ' product Updated successfully')
        return redirect('/view_arrivals')
    context = {"arrival": arrival}
    return render(request, 'edit-latest-arrivals.html', context)


def delete_arrivals(request, id):
    arrival = Arrivals.objects.get(id=id)
    if len(arrival.arrival_img) > 0:
        os.remove(arrival.arrival_img.path)
    arrival.delete()
    messages.success(request, ' Deleted successfully')
    return redirect("/view_arrivals", )


# ------------------------------------------------------------------------------------------------------------------------------

# for customer Application Views

# home page view:


def base(request):
    banner = Banner.objects.all()
    leftbanners = Left_Banner.objects.all()
    rightbanners = Right_Banner.objects.all()
    products = Product.objects.all()
    arrivals = Arrivals.objects.all()
    return render(request, 'base_cutomer.html',  {"banner": banner, "leftbanners": leftbanners, "rightbanners": rightbanners, "products": products, "arrivals": arrivals})

# all product view:


def all_product(request):
    product = Product.objects.all()
    return render(request, "all-products.html", {"product": product})

# all product shop view:

@login_required()
def all_product_shop(request):
    product = Product.objects.all()
    return render(request, "all-products-shop.html", {"product": product})

# product details view:


def product_details(request, id):
    products = Product.objects.get(id=id)

    product = Product.objects.all()
    return render(request, 'product-details.html', {"products": products, "product": product})

# product details shop view:


def product_details_shop(request, id):
    products = Product.objects.get(id=id)
    product = Product.objects.all()
    return render(request, 'product-details-shop.html', {"products": products, "product": product})

# customer register view:


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
                return redirect('/customer_login')
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
        # if fromPage == "":
        #     return render(request, 'add-customer.html')
        # else:
        #     return render(request, 'customer-register.html')


# customer login view:

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


# customer contact view:

def customer_contact(request):
    if request.method == 'POST':
        customer = Customer_Contact()
        customer.customer_name = request.POST.get("customer_name")
        customer.customer_email = request.POST.get("customer_email")
        customer.customer_subject = request.POST.get("customer_subject")
        customer.customer_comments = request.POST.get("customer_comments")
        customer.save()
        messages.success(request, ' Query received successfully')
    return render(request, 'customer-contact.html')

# add-to-cart view:

#@login_required
def add_to_cart(request,id):
    products = Product.objects.get(id=id)
    product = Product.objects.all()
    carts = None
    if request.method == 'POST':
        #cart = Add_To_Cart()
        #carts = Add_To_Cart.objects.filter(quantity=quantity)
        #carts, created=Add_To_Cart.objects.get_or_created(id=id)
        carts=Add_To_Cart()
        carts.quantity = request.objects.get("quantity")
        carts.product= Product.objects.get(id=id)
        carts.total=request.POST.get("total")
       
        # carts.quantity+=1
        carts.total=int(carts.quantity) * int(products.unit_price)
        carts.save()
        
        messages.success(request, ' Cart Added successfully')
    return render(request, 'product-details-shop.html', {"products": products,"carts":carts,"product":product})


# customer cart view:

def cart(request,id):
    products=Add_To_Cart.objects.get(id=id)
    

    return render(request, "cart.html" ,{"products":products})

# customer checkout:


def final(request,id):
    Cart=Add_To_Cart.objects.get(id=id)
    if request.method == "POST":
        check = checkout()
        check.cname=request.POST.get("cname")
        check.clast=request.POST.get("clast")
        check.caddress=request.POST.get("caddress")
        check.caddress2=request.POST.get("caddress2")
        check.ccity=request.POST.get("ccity")
        check.cstate=request.POST.get("cstate")
        check.cpin=request.POST.get("cpin")
        check.cphone=request.POST.get("cphone")
        check.cemail=request.POST.get("cemail")
        check.cart_iteam=Add_To_Cart.objects.get(id=id)
        check.pro=Product.objects.get(id=id)


        check.save()
        messages.info(request,"Order Place successfully")
        return redirect('/home')
        buff=io.BytesI()
        c=canvas.Canvas(buff, pagesize=letter, bottomup=0)
        textobj=c.beginText()
        textobj.setTextOrigin(inch, inch)
        textobj.setFont("Arial", 14)

        lines=[]
        for i in Cart:
            lines.append(i.cname)
            lines.append(i.clast)
            lines.append(i.caddress)
            lines.append(i.caddress2)
            lines.append(i.cstate)
            lines.append(i.cpin)



        c.drawText(textobj)
        c.showPage()
        c.save()
        buff.seek(0)
        return FileResponse(buff, as_attachment=True, filename="invoice.pdf")


    # temp="checkout.html"
    # context={"Cart":Cart}
    # res=HttpResponse(content_type="application/pdf")
    # res ["content-description"]='file_nam="invoice.pdf"'
    # template=get_template(temp)
    # html=template.render(context)
    # pisa_status=pisa.CreatePDF(html,dest=res)
    # if pisa_status.err:
    #     return HttpResponse("We had some Error"+html)
    # return response
    #return HttpResponse("Hi Farooq")
    return render(request, "checkout.html", {"Cart":Cart})

