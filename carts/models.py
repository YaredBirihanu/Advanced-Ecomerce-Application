from django.db import models
from store.models import Product,Variation

class Cart(models.Model):
    cart_id=models.CharField(max_length=255,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    variations=models.ManyToManyField(Variation, blank=True)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity=models.IntegerField(default='0')
    is_active=models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price*self.quantity
    
    def __unicode__(self):
        return self.product
    
    
