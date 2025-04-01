from django.contrib import admin
from .models import Payment, Order, OrderProduct

class OrderProductInline(admin.TabularInline):
    model=OrderProduct
    readonly_fields=('payments','user','quantity','product','product_price','ordered')
    extra=0

class OrderAdmin(admin.ModelAdmin):
    list_display=['order_number','first_name','phone','email','city','order_total','tax','status','is_ordered','created']
    list_filter=['status','is-ordered']
    search_fields=['order_number','first_name','last_name','phone','email']
    list_per_page=20
    inlines=[OrderProductInline]


admin.site.register(Payment)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct)
