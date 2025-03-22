from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account


class AccountAdmin(UserAdmin):
    list_dispaly=('email','first_name','last_name','username','date_joined','last_login','is_active')
    list_display_link=('email','first_name','last_name')
    readonly_fields=('date_joined','last_login')
    ordering=('-date_joined',)

    filter_horizontal=()
    list_filter=()
    fieldsets=()


admin.site.register(Account,AccountAdmin)