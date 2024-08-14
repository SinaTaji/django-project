from django.contrib import admin
from products.models import Products, Product_Brand, Product_Category, ProductCars, ProductVisited, \
    ProductGallery, Product_color, PriceByProductColor, ProductComment,suggestion


class AdminProducts(admin.ModelAdmin):
    list_display = ['title', 'price', 'is_active', 'is_delete']
    list_editable = ['is_active', 'is_delete', 'price']

class AdminCars(admin.ModelAdmin):
    list_display = ['title', 'get_car']


class AdminBrands(admin.ModelAdmin):
    list_display = ['title', 'brand_url', 'is_active']
    list_editable = ['is_active']


class AdminProductCategory(admin.ModelAdmin):
    list_display = ['title', 'url_title', 'is_active', 'is_delete', 'category']
    list_editable = ['is_active', 'is_delete', 'category']


admin.site.register(Products, AdminProducts)
admin.site.register(Product_Brand, AdminBrands)
admin.site.register(Product_Category, AdminProductCategory)
admin.site.register(ProductCars,AdminCars)
admin.site.register(ProductVisited)
admin.site.register(ProductGallery)
admin.site.register(Product_color)
admin.site.register(PriceByProductColor)
admin.site.register(ProductComment)
admin.site.register(suggestion)
