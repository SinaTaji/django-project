# Generated by Django 5.0.6 on 2024-07-01 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0027_pricebyproductcolor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricebyproductcolor',
            name='price_by_color',
            field=models.IntegerField(verbose_name='قیمت محصول بر اساس رنگ'),
        ),
    ]