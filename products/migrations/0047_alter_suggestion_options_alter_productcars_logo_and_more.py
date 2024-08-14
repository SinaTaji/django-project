# Generated by Django 5.0.6 on 2024-07-27 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0046_alter_product_brand_brand_url_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='suggestion',
            options={'verbose_name': 'محل نصب قطعه', 'verbose_name_plural': 'محل نصب قطعات'},
        ),
        migrations.AlterField(
            model_name='productcars',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='cars/image', verbose_name='لوگو خودرو'),
        ),
        migrations.DeleteModel(
            name='Product_Tags',
        ),
    ]