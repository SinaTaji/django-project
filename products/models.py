from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from User.models import User


class Product_Category(models.Model):
    category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True
                                 , verbose_name='دسته بندی والد ')
    title = models.CharField(max_length=200, verbose_name='اسم دسته بندی', db_index=True)
    url_title = models.CharField(max_length=200, verbose_name='اسم دسته بندی در url', db_index=True, blank=True,
                                 unique=True)
    is_active = models.BooleanField(default=False, verbose_name='فعال/غیرفعال')

    is_delete = models.BooleanField(default=False, verbose_name='موجود/حذف شده')
    image = models.ImageField(upload_to='products/categories/category', null=True, blank=True,
                              verbose_name='عکس دسته بندی')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.url_title = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
        return self.url_title

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class Product_Brand(models.Model):
    title = models.CharField(max_length=200, verbose_name='برند', db_index=True)
    brand_url = models.CharField(max_length=300, verbose_name='عنوان در url', db_index=True, blank=True, unique=True)
    is_active = models.BooleanField(default=False, verbose_name='فعال/غیرفعال')
    image = models.ImageField(upload_to='products/categories/brands', null=True, blank=True, verbose_name='تصویر برند')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.brand_url = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
        return self.brand_url

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برندها'


class ProductCars(models.Model):
    title = models.CharField(max_length=100, db_index=True, verbose_name='اسم خودرو')
    url_title = models.CharField(max_length=200, db_index=True, verbose_name='عنوان در url', blank=True, unique=True)
    car = models.ForeignKey('self', verbose_name='دسته بندی والد', on_delete=models.CASCADE,
                            null=True, blank=True)
    logo = models.ImageField(upload_to='cars/image', null=True, blank=True, verbose_name='لوگو خودرو')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیر فعال')

    class Meta:
        verbose_name = 'خودرو '
        verbose_name_plural = ' خودرو ها'

    def save(self, *args, **kwargs):
        self.url_title = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
        return self.url_title

    def get_car(self):
        return self.car.title if self.car else None

    get_car.short_description = 'دسته بندی'

    def __str__(self):
        return self.title


class Product_color(models.Model):
    title = models.CharField(max_length=100, verbose_name='نام رنگ')
    url_title = models.CharField(max_length=200, verbose_name='عنوان در url', db_index=True, unique=True,blank=True)
    hex_value = models.CharField(max_length=20, verbose_name='کد رنگ')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.url_title = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
        return self.url_title

    class Meta:
        verbose_name = 'رنگ محصولات'
        verbose_name_plural = 'رنگ های محصولات'


class suggestion(models.Model):
    title = models.CharField(max_length=100, verbose_name='محل نصب', db_index=True)

    class Meta:
        verbose_name = 'محل نصب قطعه'
        verbose_name_plural = 'محل نصب قطعات'

    def __str__(self):
        return self.title


class Products(models.Model):
    class Position(models.TextChoices):
        front = 'front', "جلو"
        right_front = 'right_front', "جلو راست و جلو چپ"
        right = 'right', " راست"
        left = 'left', "چپ"
        back = 'back', 'عقب'
        right_back = 'right_back', "عقب راست و عقب چپ"

    class Material(models.TextChoices):
        plastic = 'plastic', 'پلی اتیلن'
        felez = 'felez', 'فلز'
        glass = 'glass', 'شیشه'
        poly_carbonat = 'poly_carbonat', 'پلی کربنات (پلاستیک Uv)'

    class garanti(models.TextChoices):
        zemanat_none = 'zemanat_none', 'فاقد ضمانت از سمت تولید کننده میباشد'
        zemanat_1_sale = 'zemanat_1_sale', 'دارای 1 سال ضمانت رنگ میباشد'
        zemanat_5_sale = 'zemanat_5_sale', 'دارای 5 سال ضمانت رنگ میباشد'

    title = models.CharField(max_length=200, verbose_name='اسم محصول')
    short_description = models.TextField(verbose_name='توضیحات کوتاه', db_index=True)
    description = models.TextField(verbose_name='توضیحات کامل')
    price = models.IntegerField(verbose_name='قیمت')
    is_active = models.BooleanField(default=False, verbose_name='فعال/غیرفعال')
    car_products = models.ForeignKey(ProductCars, null=True, verbose_name='خودرو', db_index=True,
                                     on_delete=models.CASCADE)
    brand = models.ForeignKey(Product_Brand, null=True, db_index=True, verbose_name='برند ها', on_delete=models.CASCADE)
    Category = models.ManyToManyField(Product_Category, db_index=True, verbose_name='دسته بندی محصول')
    has_color = models.BooleanField(verbose_name='محصول دارای رنگ بندی است ؟', db_index=True, default=False)
    colors = models.ManyToManyField(Product_color, db_index=True, verbose_name="رنگ های محصول", blank=True)
    position = models.CharField(max_length=200, choices=Position.choices, verbose_name="محل نصب", null=True)
    side = models.BooleanField(default=False, verbose_name='آیا قطعه دارای جهت بندی میباشد')
    suggest = models.ManyToManyField(suggestion, verbose_name='ایجاد ارتباط برای پیشنهاد', blank=True, db_index=True)
    material = models.CharField(max_length=200, choices=Material.choices, verbose_name="جنس", null=True)
    garanti = models.CharField(max_length=200, choices=garanti.choices, verbose_name='وضعیت ضمانت', null=True)
    cars = models.CharField(max_length=500, verbose_name='مناسب برای خودرو', null=True, db_index=True)
    slug = models.SlugField(db_index=True, null=False, blank=True, allow_unicode=True, verbose_name='اسلاگ')
    image = models.ImageField(upload_to='images/uploads/', null=True, blank=True, verbose_name='تصویر محصول')
    is_delete = models.BooleanField(default=False, verbose_name='موجود/حذف شده')

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = "محصولات"

    def get_absolute_url(self):
        return reverse('products_detail_page', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
        return self.slug

    def __str__(self):
        return self.title


class PriceByProductColor(models.Model):
    products = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='محصول', db_index=True)
    colors = models.ManyToManyField(Product_color, verbose_name="رنگ ها")
    price_by_color = models.IntegerField(verbose_name='قیمت محصول بر اساس رنگ')

    def __str__(self):
        color_names = ', '.join([color.title for color in self.colors.all()])
        return f"{self.products} | رنگ ها : {color_names} | {self.price_by_color}"

    class Meta:
        verbose_name = 'قیمت محصول بر اساس رنگ'
        verbose_name_plural = "قیمت محصولات بر اساس رنگ ها "




class ProductVisited(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='کالا')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='کاربر')
    ip = models.CharField(max_length=30, verbose_name='ip کاربر')

    class Meta:
        verbose_name = 'بازدید محصول'
        verbose_name_plural = 'بازدید های محصولات'

    def __str__(self):
        return f"{self.product.title} / {self.user}"


class ProductGallery(models.Model):
    products = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='محصول')
    images = models.ImageField(upload_to='images/galleries', verbose_name='تصاویر محصول')

    def __str__(self):
        return self.products.title

    class Meta:
        verbose_name = 'تصویر گالری'
        verbose_name_plural = 'گالری تصاویر'


class ProductComment(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name="محصول")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='والد', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='زمان ثبت')
    text = models.TextField(verbose_name='متن نظر')
    is_active = models.BooleanField(default=False, verbose_name='نمایش داده شود/ نشود')

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'نظر محصول'
        verbose_name_plural = 'نظرات محصولات'
