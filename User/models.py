from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    avatar = models.ImageField(upload_to='images/user', verbose_name='تصویر پروفابل', null=True, blank=True)
    email_active_code = models.CharField(max_length=300, verbose_name='کد تااید ایمل',editable=False)
    address = models.TextField(null=True, blank=True, verbose_name='آدرس')
    about_user = models.TextField(null=True, blank=True, verbose_name='درباره شما')

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        if self.username:
            return self.username
        elif self.first_name is not '' and self.last_name is not '':
            return (f"{self.first_name} {self.last_name}")
        return self.email

