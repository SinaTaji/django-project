# Generated by Django 5.0.6 on 2024-06-19 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_productcars_short_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcars',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='cars/image', verbose_name='لوگو حودرو'),
        ),
    ]
