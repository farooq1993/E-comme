from django import forms
from django.db import models
from django.db.models import fields
from django.db.models.base import Model
from unagaapp.models import Arrivals, Category, Damaged_list, Sub_Category, Order, Transfer, Wardrobe
from django.forms import ClearableFileInput


class Category_Form(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"


class Sub_Category_Form(forms.ModelForm):
    class Meta:
        model = Sub_Category
        fields = "__all__"


# class Product_Form(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = "__all__"


class Order_Form(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"


class Damages_Form(forms.ModelForm):
    class Meta:
        model = Damaged_list
        fields = "__all__"


class Transfer_Form(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = "__all__"


# class Wardrobe_Form(forms.ModelForm):
#     class Meta:
#         model = Wardrobe
#         fields = "__all__"


class Wardrobe_Form(forms.ModelForm):
    class Meta:
        model = Wardrobe
        fields = "__all__"
        widgets = {"images": ClearableFileInput(attrs={"images": True}),
                   }


class Arrivals_Form(forms. ModelForm):
    class Meta:
        model = Arrivals
        fields = "__all__"
