from django.contrib import admin

from .models import *

# Register your models here.
class AddtocartAdmin(admin.ModelAdmin):
    display=["quantity","product"]



admin.site.register(Category)
admin.site.register(Sub_Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Damaged_list)
admin.site.register(Transfer)
admin.site.register(Add_To_Cart,AddtocartAdmin)
admin.site.register(checkout)
admin.site.register(Cart)
