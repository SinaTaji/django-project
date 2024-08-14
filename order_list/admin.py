from django.contrib import admin
from .models import Order, OrderDetail, final_payment


class Orderadmin(admin.ModelAdmin):
    list_display = ['user', 'id', 'is_paid', 'get_jalali_date','final_price']




class final_paymentadmin(admin.ModelAdmin):
    list_display = ['first_name', 'phone_number', 'send_method', 'get_jalali_date','get_time','get_order_id']


class OrderDetailadmin(admin.ModelAdmin):
    list_display = ['get_order_id','products','products_color','side','count']


admin.site.register(Order, Orderadmin)
admin.site.register(OrderDetail,OrderDetailadmin)
admin.site.register(final_payment, final_paymentadmin)
