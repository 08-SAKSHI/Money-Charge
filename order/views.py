from datetime import datetime
import razorpay
from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404, get_list_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .constants import PaymentStatus
import json
from order.models import Order,OrderMeta
import copy
# Create your views here.

@login_required
def index(request):
    orders = Order.objects.filter(user = request.user)
    return render(request,'orders/index.html',{'orders':orders})

@login_required
def order_details(request,id=None):
    order = get_object_or_404(Order,order_id=id)
    order_details = get_list_or_404(OrderMeta,order_id=id)
    return render(request, 'orders/detail.html',{'order':order,'order_details':order_details})

@csrf_exempt
def order_payment_callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=("rzp_test_SxGQ4hz6s3CCCi", "PK8TzrhaXaWBCYOl7MYqUdJN"))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()
        if not verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
            order.save()
            return render(request, "base/index.html", context={"status": order.status})
        else:
            order.status = PaymentStatus.FAILURE
            order.save()
            return render(request, "orders/payment_callback.html", context={"status": order.status})
    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        order.save()
        return render(request, "callback.html", context={"status": order.status})

@login_required
def order_account_create(request):
    if request.method == 'POST':
        form= request.POST
        error=[]
        if form.get('account_number') != form.get('confirm_account_number'):
            error.append('Account number is Not Same')
        if len(form.get('ifsc_code')) != 11:
            error.append('IFS Code is not correct')
        if int(form.get('amount')) < 1:
            error.append('Amount should be greater than 0')
        if len(error)==0:
            #create Order object and add account number and ifsc code to OrderMeta
            # order = Order.objects.create(receiver_name=form.get('receiver_name'),transaction_type=form.get('transaction_type'),status=form.get('status'),amount=form.get('amount'))
            client = razorpay.Client(auth=("rzp_test_SxGQ4hz6s3CCCi", "PK8TzrhaXaWBCYOl7MYqUdJN"))
            payment = client.order.create({'amount':int(form.get('amount'))*100, 'currency': 'INR','payment_capture': '1'})
            order = Order.objects.create(user = request.user,receiver_name=form.get('receiver_name'),transaction_type=form.get('transaction_type'),status=form.get('status'),amount=form.get('amount'),provider_order_id=payment['id'])
            order.save()
            OrderMeta.objects.create(order_id=order, key='account_number', value=form.get('account_number'))
            OrderMeta.objects.create(order_id=order, key='ifsc_code', value=form.get('ifsc_code'))
            return render(request,'orders/create.html',{'callback_url':'http://'+ request.get_host() + '/order/payment/callback/','razorpay_key':'rzp_test_SxGQ4hz6s3CCCi','order':order,'form':form,'payment':payment})
            # return HttpResponseRedirect('/')
        else:
            return render(request,'orders/create.html',{'errors':error,'form':form})
    else:
        pass
    return render(request,'orders/create.html')

@login_required
def order_UPI_create(request):
    if request.method == 'POST':
        form= request.POST
        error=[]
        if int(form.get('amount')) < 1:
            error.append('Amount should be greater than 0')
        if len(error)==0:
            order = Order.objects.create(receiver_name=form.get('receiver_name'),transaction_type=form.get('transaction_type'),status=form.get('status'),amount=form.get('amount'))
            OrderMeta.objects.create(order_id=order,key='UPI',value=form.get('Upi_Id'))
            return HttpResponseRedirect('/')
        else:
            return render(request,'orders/createUPI.html',{'form':form,'errors':error})
    return render(request,'orders/createUPI.html')

@login_required
def order_Rent_create(request):
    if request.method == 'POST':
        form= request.POST
        error=[]
        if form.get('account_number') != form.get('confirm_account_number'):
            error.append('Account number is Not Same')
        if len(form.get('ifsc_code')) != 11:
            error.append('IFS Code is not correct')
        if int(form.get('amount')) < 1:
            error.append('Amount should be greater than 0')
        if len(error)==0:
            #create Order object and add account number and ifsc code to OrderMeta
            order = Order.objects.create(receiver_name=form.get('receiver_name'),transaction_type=form.get('transaction_type'),status=form.get('status'),amount=form.get('amount'))
            OrderMeta.objects.create(order_id=order,key='account_number',value=form.get('account_number'))
            OrderMeta.objects.create(order_id=order,key='ifsc_code',value=form.get('ifsc_code'))
            return HttpResponseRedirect('/')
        else:
            return render(request,'orders/create.html',{'errors':error,'form':form})
    else:
        pass
    return render(request,'orders/createRent.html')

@login_required
def order_Vendor_create(request):
    if request.method == 'POST':
        form= request.POST
        error=[]
        if form.get('account_number') != form.get('confirm_account_number'):
            error.append('Account number is Not Same')
        if len(form.get('ifsc_code')) != 11:
            error.append('IFS Code is not correct')
        if int(form.get('amount')) < 1:
            error.append('Amount should be greater than 0')
        if len(error)==0:
            #create Order object and add account number and ifsc code to OrderMeta
            order = Order.objects.create(receiver_name=form.get('receiver_name'),transaction_type=form.get('transaction_type'),status=form.get('status'),amount=form.get('amount'))
            OrderMeta.objects.create(order_id=order,key='account_number',value=form.get('account_number'))
            OrderMeta.objects.create(order_id=order,key='ifsc_code',value=form.get('ifsc_code'))
            return HttpResponseRedirect('/')
        else:
            return render(request,'orders/create.html',{'errors':error,'form':form})
    else:
        pass
    return render(request,'orders/createVendor.html')