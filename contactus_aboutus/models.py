from django.db import models


class ContactUsModel(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان پیام')
    full_name = models.CharField(max_length=200, verbose_name='نام کامل')
    email = models.EmailField(max_length=200, verbose_name='ایمیل')
    message = models.TextField(verbose_name='متن پیام کاربر')
    is_read = models.BooleanField(default=False, verbose_name='خوانده شده / نشده')
    date = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")
    response_message = models.TextField(verbose_name='پیام ادمین')

    class Meta :
        verbose_name = 'تماس با ما'
        verbose_name_plural = 'لیست تماس با ما'

    def __str__(self):
        return self.title