from django.db import models
from jalali_date import date2jalali
from User.models import User

class ArticleCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name='اسم دسته بندی')
    url_title = models.CharField(max_length=100, verbose_name='عنوان در url', unique=True)
    category = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='دسته بندی والد', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = ' دسته بندی مقالات'
        verbose_name_plural = 'دسته بندی های مقالات'

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    url_title = models.CharField(max_length=200, verbose_name='عنوان در url', unique=True)
    auther = models.ForeignKey(User,on_delete=models.CASCADE,null=True,editable=False, verbose_name='نویسنده')
    short_description = models.CharField(max_length=400, verbose_name='توضیحات کوتاه')
    text = models.TextField(verbose_name='توضیحات کامل')
    selected_category = models.ManyToManyField(ArticleCategory, verbose_name="دسته بندی ها")
    image = models.ImageField(upload_to='images/article', verbose_name='عکس مقاله')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'

    def __str__(self):
        return self.title

    def get_jalali_date (self):
        return date2jalali(self.create_date)

    def get_jalali_time(self):
        return self.create_date.strftime('%H:%M')

class ArticleComment(models.Model):
    article = models.ForeignKey(Article,on_delete=models.CASCADE,verbose_name="مقاله")
    parent = models.ForeignKey('self',on_delete=models.CASCADE,verbose_name='والد',null=True, blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='کاربر')
    create_date = models.DateTimeField(auto_now_add=True,verbose_name='زمان ثبت')
    text = models.TextField(verbose_name='متن نظر')
    is_active = models.BooleanField(default=False, verbose_name='نمایش داده شود/ نشود')

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'نظر مقاله'
        verbose_name_plural = 'نظرات مقالات'