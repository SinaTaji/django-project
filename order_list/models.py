from django.db import models
from User.models import User
from products.models import Products, Product_color, PriceByProductColor
from jalali_date import date2jalali


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر', null=True, blank=True)
    session = models.CharField(max_length=100, verbose_name="کاربر فعلی", null=True, blank=True)
    is_paid = models.BooleanField(default=False, verbose_name='پرداخت شده/ نشده')
    payment_date = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ ثبت خرید')
    final_price = models.IntegerField(null=True, blank=True, verbose_name='مبلغ پرداخت شده نهایی کاربر')

    def calculate_total(self):
        total = 0
        if self.is_paid:
            for order_detail in self.orderdetail_set.all():
                total += order_detail.price
        else:
            for order_detail in self.orderdetail_set.all():
                price_by_color = PriceByProductColor.objects.filter(
                    products_id=order_detail.products_id,
                    colors=order_detail.products_color
                ).first()
                if price_by_color:
                    price = price_by_color.price_by_color
                else:
                    price = order_detail.products.price
                total += price * order_detail.count
        return total

    def __str__(self):
        if self.user:
            return str(self.user.username)
        return str(self.session)

    def get_jalali_date(self):
        return date2jalali(self.payment_date)

    get_jalali_date.short_description = 'تاریخ ثبت خرید'

    class Meta:
        verbose_name = 'سبد خرید کاربر'
        verbose_name_plural = 'سبد های خرید کاربران'


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سبد خرید')
    products = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='محصول')
    products_color = models.ForeignKey(Product_color, verbose_name='رنگ محصول', on_delete=models.CASCADE, null=True)
    side = models.CharField(max_length=10, choices=[('left', 'چپ'), ('right', 'راست')], null=True,
                            blank=True)
    final_price = models.IntegerField(null=True, blank=True, verbose_name='قیمت محصول')
    count = models.IntegerField(verbose_name='تعداد محصولات')

    def get_total_price(self):
        return self.count * self.products.price

    def __str__(self):
        return str(self.order)

    def get_order_id(self):
        return int(self.order.id)

    get_order_id.short_description = 'فاکتور'

    class Meta:
        verbose_name = 'جزئیات سبد خرید'
        verbose_name_plural = 'لیست جزئیات سبد های خرید '


class final_payment(models.Model):
    send_method = [
        ("post", 'پست'),
        ("terminal", 'ترمینال'),
        ("barbary", 'باربری'),
        ("t_pax", 'تیپاکس'),
    ]
    first_name = models.CharField(max_length=50, verbose_name='نام')
    last_name = models.CharField(max_length=50, verbose_name='نام خانوادگی')
    address = models.TextField(verbose_name='آدرس')
    postal_code = models.CharField(max_length=20,verbose_name='کد پستی', null=True, blank=True)
    phone_number = models.CharField(max_length=11,verbose_name='شماره موبایل')
    send_method = models.CharField(max_length=20, choices=send_method, default='post', verbose_name="روش ارسال")
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت خرید')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='شماره فاکتور', null=True, blank=True,
                              editable=False)

    class Meta:
        verbose_name = 'مشخصات خرید کننده'
        verbose_name_plural = 'مشخصات خرید کنندگان'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_jalali_date(self):
        return date2jalali(self.payment_date)

    get_jalali_date.short_description = 'تاریخ ثبت خرید'

    def get_order_id(self):
        return self.order.id if self.order else 'No Order'

    get_order_id.short_description = 'فاکتور'

    def get_time(self):
        return self.payment_date.time().strftime('%H:%M:%S')

    get_time.short_description = 'ساعت'
