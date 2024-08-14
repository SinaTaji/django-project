# Generated by Django 5.0.6 on 2024-07-27 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0045_alter_product_category_url_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_brand',
            name='brand_url',
            field=models.CharField(blank=True, db_index=True, default='koob', max_length=300, unique=True, verbose_name='عنوان در url'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product_category',
            name='url_title',
            field=models.CharField(blank=True, db_index=True, max_length=200, unique=True, verbose_name='اسم دسته بندی در url'),
        ),
        migrations.AlterField(
            model_name='product_color',
            name='url_title',
            field=models.CharField(blank=True, db_index=True, max_length=200, unique=True, verbose_name='عنوان در url'),
        ),
        migrations.AlterField(
            model_name='productcars',
            name='url_title',
            field=models.CharField(blank=True, db_index=True, max_length=200, unique=True, verbose_name='عنوان در url'),
        ),
    ]
