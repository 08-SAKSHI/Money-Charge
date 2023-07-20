from email.policy import default
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Order(models.Model):
    order_id = models.AutoField(primary_key=True,editable=False)
    user = models.ForeignKey(User,on_delete = models.DO_NOTHING,null = True)
    receiver_name = models.CharField(max_length=255,null=True)
    transaction_type = models.CharField(max_length=25)
    status = models.CharField(max_length=25)
    amount = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    payment_status = models.CharField(max_length=25, default='pending',null=True)
    provider_order_id = models.CharField(max_length=40, null=True,blank=False)
    payment_id = models.CharField(max_length=36, null=True,blank=True)
    signature_id = models.CharField(max_length=128, null=True,blank=True)

    def __str__(self):
        return self.receiver_name

class OrderMeta(models.Model):
    order_id = models.ForeignKey(Order,on_delete=models.CASCADE)
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"Key: {self.key} Value:{self.value}"
