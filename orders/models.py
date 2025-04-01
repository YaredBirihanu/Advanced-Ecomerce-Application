from django.db import models
from accounts.models import Account
from store.models import Product, Variation


class Payment(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    payment_id=models.IntegerField()
    payment_method=models.CharField(max_length=255)
    amonunt_paid=models.FloatField()
    status=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.payment_method

class Order(models.Model):
    STATUS=(
        ('New','New'),
        ('Accepted','Accepted'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled'),
  
    )
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    payment=models.ForeignKey(Payment,on_delete=models.SET_NULL,null=True,blank=True)
    order_number=models.CharField(max_length=20)
    full_name=models.CharField(max_length=50)
    phone_number=models.CharField(max_length=15)
    email=models.EmailField()
    address_line_1=models.CharField(max_length=50)
    address_line_2=models.CharField(max_length=50,blank=True)
    country=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    order_note=models.TextField(max_length=50,blank=True)
    order_total=models.FloatField()
    status=models.CharField(max_length=50,choices=STATUS,default='New')
    ip=models.CharField(max_length=50,blank=True)
    is_ordered=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name
    
class OrderProduct(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    payment=models.ForeignKey(Payment,on_delete=models.SET_NULL,null=True,blank=True)
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    variation=models.ForeignKey(Variation,on_delete=models.CASCADE)
    color=models.CharField(max_length=50)
    size=models.CharField(max_length=50)
    quantity=models.IntegerField()
    ordered=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name