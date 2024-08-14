# Generated by Django 3.2.25 on 2024-06-12 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_rename_brand_product_brand_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=100, verbose_name='اسم خودرو')),
                ('url_title', models.CharField(db_index=True, max_length=200, verbose_name='عنوان در url')),
                ('car', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.productcars', verbose_name='دسته بندی والد')),
                ('car_products', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.products', verbose_name='خودرو')),
            ],
            options={
                'verbose_name': 'خودرو ها',
                'verbose_name_plural': 'خودرو',
            },
        ),
    ]