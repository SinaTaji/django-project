# Generated by Django 3.2.25 on 2024-06-10 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_product_brand_brand_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='selected_category',
            field=models.ManyToManyField(related_name='cat', to='products.Product_Category', verbose_name='دسته بندی'),
        ),
    ]
