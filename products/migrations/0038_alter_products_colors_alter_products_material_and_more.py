# Generated by Django 5.0.6 on 2024-07-13 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0037_remove_products_sugest_product_category_sugest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='colors',
            field=models.ManyToManyField(blank=True, db_index=True, null=True, to='products.product_color', verbose_name='رنگ های محصول'),
        ),
        migrations.AlterField(
            model_name='products',
            name='material',
            field=models.CharField(choices=[('plastic', 'پلی اتیلن'), ('felez', 'فلز'), ('glass', 'شیشه'), ('poly_carbonat', 'پلی کربنات (پلاستیک Uv)')], max_length=200, null=True, verbose_name='جنس'),
        ),
        migrations.AlterField(
            model_name='products',
            name='position',
            field=models.CharField(choices=[('front', 'جلو'), ('right_front', 'جلو راست و جلو چپ'), ('right', ' راست'), ('left', 'چپ'), ('back', 'عقب'), ('right_back', 'عقب راست و عقب چپ')], max_length=200, null=True, verbose_name='محل نصب'),
        ),
    ]
