from django.urls import path
from django.urls.conf import include
from django.urls.resolvers import URLPattern
from unagaproject.settings import DEBUG
from . import views
from unagaapp import views


from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('', views.login),
    path('', views.index),
    path('index', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard', views.dashboard),


    path('add_category', views.add_category),
    path('view_category', views.view_category),
    path('edit_category/<int:id>', views.edit_category),
    path('delete_category/<int:id>', views.delete_category),
    path('update_category/<int:id>', views.update_category),


    path('add_sub_category', views.add_sub_category),
    path('view_sub_category', views.view_sub_category),
    path('edit_sub_category/<int:id>', views.edit_sub_category),
    path('delete_sub_category/<int:id>', views.delete_sub_category),
    path('update_sub_category/<int:id>', views.update_sub_category),

    path('add_product', views.add_product),
    path('view_product', views.view_product),
    path('edit_product/<int:id>', views.edit_product),
    path('delete_product/<int:id>', views.delete_product),

    path('add_order', views.add_order),
    path('manage_order', views.manage_order),
    path('edit_order/<int:id>', views.edit_order),
    path('delete_order/<int:id>', views.delete_order),

    path('manage_inventory', views.manage_inventory),
    path('edit_inventory/<int:id>', views.edit_inventory),


    path('add_damaged_list/<int:id>', views.add_damaged_list),
    path('view_damaged_list', views.view_damaged_list),
    path('edit_damaged_list/<int:id>', views.edit_damaged_list),
    path('delete_damaged_list/<int:id>', views.delete_damaged_list),


    path('add_transfer', views.add_transfer),
    path('manage_transfer', views.manage_transfer),
    path('delete_transfer/<int:id>', views.delete_transfer),

    path('add_banner', views.add_banner),
    path('view_banner', views.view_banner),
    path('edit_banner/<int:id>', views.edit_banner),
    path('delete_banner/<int:id>', views.delete_banner),

    path('add_leftbanner', views.add_leftbanner),
    path('view_leftbanner', views.view_leftbanner),
    path('edit_leftbanner/<int:id>', views.edit_leftbanner),
    path('delete_leftbanner/<int:id>', views.delete_leftbanner),

    path('add_rightbanner', views.add_rightbanner),
    path('view_rightbanner', views.view_rightbanner),
    path('edit_rightbanner/<int:id>', views.edit_rightbanner),
    path('delete_rightbanner/<int:id>', views.delete_rightbanner),

    path('add_customer', views.customer_register),
    # path('view_customer', views.view_customer),
    # path('edit_customer/<int:id>', views.edit_customer),
    # path('delete_customer/<int:id>', views.delete_customer),

    path('add_user', views.add_user),
    path('view_user', views.view_user),
    path('edit_user/<int:id>', views.edit_user),
    path('delete_user/<int:id>', views.delete_user),

    path('add_wardrobe', views.add_wardrobe),
    path('view_wardrobe', views.view_wardrobe),
    path('delete_wardrobe/<int:id>', views.delete_wardrobe),

    path('add_arrivals', views.add_arrivals),
    path('view_arrivals', views.view_arrivals),
    path('edit_arrivals/<int:id>', views.edit_arrivals),
    path('delete_arrivals/<int:id>', views.delete_arrivals),

    # customer Application URLS
    path("home", views.base, name="home"),
    path("all_product", views.all_product, name="all_product"),
    path("all_product_shop", views.all_product_shop, name="all_product_shop"),
    path("product_details/<int:id>", views.product_details, name="product_details"),
    path("product_details_shop/<int:id>",
         views.product_details_shop, name="product_details_shop"),
    path('customer_login', views.customer_login, name="customer_login"),
    path('customer_register', views.customer_register, name="customer_register"),
    path('customer_contact', views.customer_contact, name="customer_contact"),
    path('add_to_cart/<int:id>', views.add_to_cart, name="add_to_cart"),
    path('cart/<int:id>', views.cart, name="cart"),
    #path('checkout', views.checkout, name="checkout")
    path("final/<int:id>",views.final, name="final")


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
