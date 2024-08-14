from django.db import models


class Link_Boxes(models.Model):
    title = models.CharField(max_length=100, verbose_name="عنوان باکس")

    class Meta:
        verbose_name = 'عنوان فوتر'
        verbose_name_plural = 'عناوین فوتر ها'

    def __str__(self):
        return self.title


class SiteFooter(models.Model):
    box = models.ForeignKey(Link_Boxes, on_delete=models.CASCADE, null=True, blank=True, verbose_name='والد')
    title = models.CharField(max_length=200, verbose_name='عنوان')
    url_title = models.CharField(max_length=200, verbose_name='عنوان در url', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='فعال غیر فعال')

    class Meta:
        verbose_name = 'لینک فوتر'
        verbose_name_plural = 'لینک های فوتر ها'

    def __str__(self):
        return self.title


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, verbose_name='اسم سایت')
    site_url = models.CharField(max_length=200, verbose_name='عنوان در url')
    address = models.CharField(max_length=300, verbose_name='آدرس')
    phone = models.CharField(max_length=100, verbose_name='شماره تلفن')
    email = models.CharField(max_length=100, verbose_name='ایمیل')
    about_us = models.TextField(verbose_name='متن درباره ما')
    copy_right = models.CharField(max_length=300, verbose_name='متن کپی رایت')
    site_logo = models.ImageField(upload_to='uploads/site_logo', verbose_name='لوگو')
    is_active = models.BooleanField(default=False, verbose_name="فعال/غیر فعال")

    class Meta:
        verbose_name = 'تنظیم سایت'
        verbose_name_plural = 'تنظیمات سایت'

    def __str__(self):
        return self.site_name


class SiteBanner(models.Model):
    class Position(models.TextChoices):
        home = 'home', 'خانه'
        products = 'products', 'محصولات'
        articles = 'articles', 'مقالات'

    title = models.CharField(max_length=200, verbose_name='نام بنر')
    url_title = models.CharField(max_length=200, verbose_name='آدرس بنر', null=True, blank=True)
    position = models.CharField(max_length=200, choices=Position.choices, verbose_name='در کدام صفحه نمایش داده شود')
    image = models.ImageField(upload_to='baners/images', verbose_name='تصویر بنر')
    is_active = models.BooleanField(verbose_name='فعال/غیرفعال', default=True)

    class Meta:
        verbose_name = 'بنر تبلیغاتی'
        verbose_name_plural = 'بنر های تبلیغاتی'

    def __str__(self):
        return self.title


class q_and_answer(models.Model):
    question = models.TextField(verbose_name='سوال')
    answer = models.TextField(verbose_name='پاسخ به سوال')

    class Meta:
        verbose_name = 'پرسش و پاسخ'
        verbose_name_plural = 'پرس ها و پاسخ های متداول'

    def __str__(self):
        return self.question