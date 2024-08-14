# Generated by Django 3.2.25 on 2024-06-09 10:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20240609_1329'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product_Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(db_index=True, max_length=200, null=True, verbose_name='برچسب')),
                ('Product_Tag', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.products', verbose_name='برچسب ها')),
            ],
            options={
                'verbose_name': 'برچسب',
                'verbose_name_plural': 'برچسب ها',
            },
        ),
    ]