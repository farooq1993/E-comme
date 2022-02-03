from django.db import models
from django.db.models.fields import CharField, IntegerField
from django.core.files.storage import FileSystemStorage
from datetime import datetime, date
import os

# Create your models here.

# ---------------------------------------------------------------------------------


class Category(models.Model):
    add_category = models.CharField(max_length=120, null=True)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.add_category

# ------------------------------------------------------------------------------------


class Sub_Category(models.Model):
    add_category = models.CharField(max_length=120, null=True)
    sub = models.CharField(max_length=120, null=True)

    class Meta:
        db_table = 'sub_category'

    def __str__(self):
        return self.add_sub

# ------------------------------------------------------------------------------------


def filepath(request, filename):
    old_filename = filename
    return os.path.join(filename)

# -------------------------------------------------------------------------------------


class Product(models.Model):
    product_name = models.CharField(max_length=120, null=True)
    product_code = models.IntegerField(null=True)
    description = models.TextField(null=True)
    categories = models.CharField(max_length=100, null=True)
    sub_categories = models.CharField(max_length=100, null=True)
   # categories = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    # sub_categories = models.ForeignKey(
    #     Sub_Category, on_delete=models.CASCADE, null=True)
    # brands = models.CharField(max_length=100, null=True)
    fabric = models.CharField(max_length=100, null=True)
    work = models.CharField(max_length=100, null=True)
    fabric_care = models.CharField(max_length=100, null=True)
    variant_color = models.CharField(max_length=100, null=True)
    sizes = models.CharField(max_length=10, null=True)
    unit_price = models.CharField(max_length=10, null=True)
    purchase_price = models.CharField(max_length=10, null=True)
    tax = models.CharField(max_length=10, null=True)
    gst = models.CharField(max_length=10, null=True)
    discount = models.CharField(max_length=10, null=True)
    total_quantity = models.CharField(max_length=10, null=True)
    meta_title = models.CharField(max_length=100, null=True)
    meta_description = models.TextField(null=True)
    image1 = models.FileField(upload_to=filepath, null=True, blank=True)
    image2 = models.FileField(upload_to=filepath, null=True, blank=True)
    image3 = models.FileField(upload_to=filepath, null=True, blank=True)
    image4 = models.FileField(upload_to=filepath, null=True, blank=True)

    class Meta:
        db_table = 'product'

    def __str__(self):
        return self.product_name


class add_quantity(models.Model):
    add_qty = models.IntegerField(null=True)
    prod_qty = models.ForeignKey(Product, on_delete=models.CASCADE)

# -------------------------------------------------------------------------------------------------------------------------


class Order(models.Model):
    customer_name = models.CharField(max_length=120, null=True)
    mobile_no = models.PositiveBigIntegerField(null=True, blank=True)
    product_name = models.CharField(max_length=120, null=True)
    product_code = models.CharField(max_length=10, null=True)
    ref_no = models.CharField(max_length=10, null=True)
    created_on = models.DateField(null=True, blank=True)
    purchase_price = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = 'order'

    def __str__(self):
        return self.customer_name


# ----------------------------------------------------------------------------------------------------------------------------


class Damaged_list(models.Model):
    product_name = models.CharField(max_length=120, null=True)
    product_code = models.IntegerField(null=True)
    categories = models.CharField(max_length=100, null=True)
    sub_categories = models.CharField(max_length=100, null=True)
    unit_price = models.CharField(max_length=10, null=True)
    purchase_price = models.CharField(max_length=10, null=True)
    total_quantity = models.CharField(max_length=10, null=True)
    damaged_quantity = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = 'Damages'

    def __str__(self):
        return self.damaged_quantity


# -----------------------------------------------------------------------------------------------------------------------------

# class Register(models.Model):
#     username = models.CharField(max_length=150, null=True)
#     email = models.CharField(max_length=150, null=True)
#     password = models.CharField(max_length=150, null=True)
#     confirm_password = models.CharField(max_length=150, null=True)

#     class Meta:
#         db_table = 'register'

# -------------------------------------------------------------------------------------------------------------------------------


class Transfer(models.Model):
    date = models.DateField(null=True)
    product_name = models.CharField(max_length=120, null=True)
    categories = models.CharField(max_length=100, null=True)
    sub_categories = models.CharField(max_length=100, null=True)
    select_branch1 = models.CharField(max_length=100, null=True)
    quantity = models.CharField(max_length=10, null=True)
    select_branch2 = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'transfer'

    def __str__(self):
        return self.date

# ---------------------------------------------------------------------------------------------------------------------------------


class Banner(models.Model):
    banner_name = models.CharField(max_length=120, null=True)
    banner_image1 = models.FileField(upload_to=filepath, null=True, blank=True)
    banner_image2 = models.FileField(upload_to=filepath, null=True, blank=True)
    banner_image3 = models.FileField(upload_to=filepath, null=True, blank=True)
    banner_image4 = models.FileField(upload_to=filepath, null=True, blank=True)
    banner_image5 = models.FileField(upload_to=filepath, null=True, blank=True)
    banner_content = models.TextField(null=True)
    banner_url = models.URLField(max_length=200, null=True)

    class Meta:
        db_table = 'banner'

    def __str__(self):
        return self.banner_name


class Left_Banner(models.Model):
    leftbanner_name = models.CharField(max_length=120, null=True)
    leftbanner_image1 = models.FileField(
        upload_to=filepath, null=True, blank=True)
    leftbanner_image2 = models.FileField(
        upload_to=filepath, null=True, blank=True)
    leftbanner_content = models.TextField(null=True)
    leftbanner_url = models.URLField(max_length=200, null=True)

    class Meta:
        db_table = 'left_banner'

    def __str__(self):
        return self.leftbanner_name


class Right_Banner(models.Model):
    rightbanner_name = models.CharField(max_length=120, null=True)
    rightbanner_image1 = models.FileField(
        upload_to=filepath, null=True, blank=True)
    rightbanner_image2 = models.FileField(
        upload_to=filepath, null=True, blank=True)
    rightbanner_content = models.TextField(null=True)
    rightbanner_url = models.URLField(max_length=200, null=True)

    class Meta:
        db_table = 'right_banner'

    def __str__(self):
        return self.rightbanner_name

# ------------------------------------------------------------------------------------------------------------------------------------


# class Customer(models.Model):
#     customer_name = models.CharField(max_length=120, null=True)
#     customer_mobile = models.PositiveBigIntegerField(null=True, blank=True)
#     customer_email = models.EmailField(max_length=254, null=True)
#     customer_address = models.TextField(null=True)
#     customer_username = models.CharField(max_length=120, null=True)
#     customer_password = models.CharField(max_length=100, null=True)

#     class Meta:
#         db_table = 'customer'

#     def __str__(self):
#         return self.customer_name

# -----------------------------------------------------------------------------------------------------------------------------------


class Unaga_user(models.Model):
    user_name = models.CharField(max_length=120, null=True)
    user_mobile = models.PositiveBigIntegerField(null=True, blank=True)
    user_username = models.CharField(max_length=120, null=True)
    user_password = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'unaga_user'

    def __str__(self):
        return self.user_name


# -------------------------------------------------------------------------------------------------------------------------------------


class Wardrobe(models.Model):
    customer_name = models.CharField(max_length=120, null=True)
    mobile_no = models.PositiveBigIntegerField(null=True, blank=True)
    alt_mobile = models.PositiveBigIntegerField(null=True, blank=True)
    email_id = models.EmailField(max_length=254, null=True)
    no_dressess = models.CharField(max_length=120, null=True)
    images = models.FileField(upload_to=filepath, blank=True, null=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    wardrobe_no = models.CharField(max_length=120, null=True)
    reciever_name = models.CharField(max_length=120, null=True)

    class Meta:
        db_table = 'wardrobe'

    def __str__(self):
        return self.customer_name


# class Wardrobe(models.Model):
#     images = models.FileField(upload_to=filepath, blank=True, null=True)

#     class Meta:
#         db_table = 'wardrobe'


# ------------------------------------------------------------------------------------------------------------------------------------
# latest Arrilavs

class Arrivals(models. Model):
    arrival_img = models.FileField(
        upload_to=filepath, null=True, blank=True)
    arrival_content = models.TextField(null=True)
    arrival_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'arrivals'

    def __str__(self):
        return self.arrival_img

# --------------------------------------------------------------------------------------------------------------------------------
# customer models


class Customer_Register(models.Model):
    customer_username = models.CharField(max_length=150, null=True)
    customer_email = models.EmailField(max_length=150, null=True)
    customer_password = models.CharField(max_length=150, null=True)
    customer_confirm_password = models.CharField(max_length=150, null=True)

    class Meta:
        db_table = 'customer_register'

    def __str__(self):
        return self.customer_username


class Customer_Contact(models.Model):
    customer_name = models.CharField(max_length=150, null=True)
    customer_email = models.EmailField(max_length=150, null=True)
    customer_subject = models.CharField(max_length=150, null=True)
    customer_comments = models.CharField(max_length=150, null=True)

    class Meta:
        db_table = 'customer_contact'

    def __str__(self):
        return self.customer_name


class Add_To_Cart(models.Model):
    user=models.ForeignKey(Customer_Register,on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0)
    product=models.ForeignKey(Product,on_delete=models.CASCADE, null=True)
    total=models.FloatField()



    class Meta:
        db_table = 'add_to_cart'

    def __str__(self):
        return str(self.quantity)

class Cart(models.Model):
    qty=models.ForeignKey(Add_To_Cart, on_delete=models.CASCADE)

    def __str__(self):
        return self.qty
  

class checkout(models.Model):
    cname=models.CharField(max_length=100)
    clast=models.CharField(max_length=100)
    caddress=models.CharField(max_length=300)
    caddress2=models.CharField(max_length=100)
    ccity=models.CharField(max_length=100)
    cstate=models.CharField(max_length=100)
    cpin=models.IntegerField()
    cphone=models.IntegerField()
    cemail=models.CharField(max_length=100)
    #total_amount=models.ForeignKey(Add_To_Cart, on_delete=models.CASCADE)
    pro=models.ForeignKey(Product, on_delete=models.CASCADE)

    


    def __str__(self):
        return self.cname
# --------------------------------------------------------------------------------------------------------------------------------
