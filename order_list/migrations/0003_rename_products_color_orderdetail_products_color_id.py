# Generated by Django 5.0.6 on 2024-06-30 20:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_list', '0002_orderdetail_products_color'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderdetail',
            old_name='products_color',
            new_name='products_color_id',
        ),
    ]
