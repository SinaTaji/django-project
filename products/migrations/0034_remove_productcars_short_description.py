# Generated by Django 5.0.6 on 2024-07-03 19:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0033_remove_productcars_car_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productcars',
            name='short_description',
        ),
    ]
