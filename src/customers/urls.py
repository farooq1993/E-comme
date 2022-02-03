from django.urls import path

from django.urls.resolvers import URLPattern
from unagaproject.settings import DEBUG
from . import views


from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.base),
    path("all_product", views.all_product, name="all_product"),
    path("product_details/<int:id>", views.product_details, name="product_details"),
    path('customer_login', views.customer_login),
    path('customer_register', views.customer_register),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
