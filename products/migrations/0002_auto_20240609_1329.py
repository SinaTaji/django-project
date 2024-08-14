# Generated by Django 3.2.25 on 2024-06-09 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product_Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(db_index=True, max_length=200, verbose_name='برند')),
                ('is_active', models.BooleanField(default=False, verbose_name='فعال/غیرفعال')),
            ],
            options={
                'verbose_name': 'برند',
                'verbose_name_plural': 'برندها',
            },
        ),
        migrations.CreateModel(
            name='Product_Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=200, verbose_name='اسم دسته بندی')),
                ('url_title', models.CharField(db_index=True, max_length=200, verbose_name='اسم دسته بندی در url')),
                ('is_active', models.BooleanField(default=False, verbose_name='فعال/غیرفعال')),
                ('is_delete', models.BooleanField(default=False, verbose_name='موجود/حذف شده')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی ها',
            },
        ),
        migrations.AlterField(
            model_name='products',
            name='title',
            field=models.CharField(max_length=200, verbose_name='اسم محصول'),
        ),
        migrations.AddField(
            model_name='products',
            name='Category',
            field=models.ManyToManyField(db_index=True, to='products.Product_Category', verbose_name='دسته بندی محصول'),
        ),
        migrations.AddField(
            model_name='products',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.product_brand', verbose_name='برند ها'),
        ),
    ]