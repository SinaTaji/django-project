# Generated by Django 5.0.6 on 2024-06-19 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_productcars_car_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcars',
            name='short_description',
            field=models.TextField(default='ادامه مطالب', verbose_name='توضیحات کوتاه'),
        ),
    ]
