# Generated by Django 3.2.25 on 2024-06-10 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_products_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_category',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.product_category', verbose_name='دسته بندی والد '),
        ),
    ]
