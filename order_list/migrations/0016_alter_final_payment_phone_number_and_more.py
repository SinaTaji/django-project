# Generated by Django 5.0.6 on 2024-07-29 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_list', '0015_alter_final_payment_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='final_payment',
            name='phone_number',
            field=models.CharField(max_length=11, verbose_name='شماره موبایل'),
        ),
        migrations.AlterField(
            model_name='final_payment',
            name='postal_code',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='کد پستی'),
        ),
    ]
