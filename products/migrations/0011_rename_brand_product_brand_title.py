# Generated by Django 3.2.25 on 2024-06-10 13:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_products_selected_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product_brand',
            old_name='brand',
            new_name='title',
        ),
    ]