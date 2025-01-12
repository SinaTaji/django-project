# Generated by Django 3.2.25 on 2024-06-13 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=100, verbose_name='اسم سایت')),
                ('site_url', models.CharField(max_length=200, verbose_name='عنوان در url')),
                ('address', models.CharField(max_length=300, verbose_name='آدرس')),
                ('phone', models.CharField(max_length=100, verbose_name='شماره تلفن')),
                ('email', models.CharField(max_length=100, verbose_name='ایمیل')),
                ('about_us', models.TextField(max_length=100, verbose_name='متن درباره ما')),
                ('copy_right', models.CharField(max_length=300, verbose_name='متن کپی رایت')),
                ('site_logo', models.ImageField(upload_to='', verbose_name='لوگو')),
                ('is_active', models.BooleanField(default=False, verbose_name='فعال/غیر فعال')),
            ],
            options={
                'verbose_name': 'تنظیم سایت',
                'verbose_name_plural': 'تنظیمات سایت',
            },
        ),
    ]
