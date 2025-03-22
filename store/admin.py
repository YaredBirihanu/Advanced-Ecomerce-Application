from django.contrib import admin
from .models import Product,Variation


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stocks','category','modified_date','is_available')
    prepopulated_fields = {'slug':('product_name',)}
    list_filter = ('category', 'is_available', 'created_date','modified_date')
    search_fields = ('product_name', 'price', 'category__name')
    ordering = ('-created_date',)
    readonly_fields = ('created_date','modified_date')

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active','created_date')
    list_editable=('is_active',)
    list_filter = ('product', 'variation_category',)

admin.site.register(Product,ProductAdmin)
admin.site.register(Variation,VariationAdmin)
