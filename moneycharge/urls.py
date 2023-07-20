"""moneycharge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from helloworld import views as helloworld_views
from order import views as order_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',helloworld_views.index,name='index'),
    path('hello',helloworld_views.hello,name="hello"),
    path('orders/',order_views.index,name="order"),    
    path('order/<int:id>/', order_views.order_details,name="order_detail"),
    path('order/create/',order_views.order_account_create,name="create_order"),
    path('order/createUPI/',order_views.order_UPI_create,name="create_upi"),
    path('order/createRent/', order_views.order_Rent_create, name="create_rent"),
    path('order/createVendor/', order_views.order_Vendor_create, name="create_vendor"),
    path('order/payment/callback/',order_views.order_payment_callback,name="payment_callback"),
    path('accounts/', include('allauth.urls')),
    path("a", include("django_browser_reload.urls")),
]
