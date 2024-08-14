# Generated by Django 5.0.6 on 2024-07-13 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0038_alter_products_colors_alter_products_material_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='main_position',
            field=models.CharField(blank=True, choices=[('left', 'راننده (L) چپ'), ('right', 'شاگرد (R) راست')], max_length=200, null=True, verbose_name='جهت قطعه'),
        ),
    ]
