from Lib.django.http.response import JsonResponse
from Lib.django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from products.forms import CommentForm
from products.models import Products, Product_Category, Product_Brand, ProductCars, ProductVisited, ProductGallery, \
    PriceByProductColor, ProductComment
from site_setting.models import SiteBanner
from utils.get_user_ip import get_user_ip
from utils.convertor import grouped
from django.db.models import Prefetch


class ProductsListView(ListView):
    model = Products
    template_name = 'products/products.html'
    paginate_by = 80
    context_object_name = 'products'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductsListView, self).get_context_data(*args, **kwargs)
        query = Products.objects.all()
        product: Products = query.order_by('-price').first()
        db_max_price = product.price if product is not None else 10000000
        context['db_max_price'] = db_max_price
        context['start_price'] = self.request.GET.get('start_price') or 0
        context['end_price'] = self.request.GET.get('end_price') or db_max_price
        context['banners'] = SiteBanner.objects.filter(is_active=True, position__iexact=SiteBanner.Position.products)
        return context

    def get_queryset(self):
        query = super(ProductsListView, self).get_queryset()
        category_name = self.kwargs.get('categorys')
        brand_name = self.kwargs.get('brand')
        car_name = self.kwargs.get('cars')
        if car_name:
            query = query.filter(car_products__url_title__iexact=car_name, is_active=True)
        if brand_name:
            query = query.filter(brand__brand_url__iexact=brand_name, is_active=True)
        if category_name:
            query = query.filter(Category__url_title__iexact=category_name, is_active=True)
        return query


class ProductsDetailView(DetailView):
    model = Products
    template_name = 'products/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_product = self.object
        user_ip = get_user_ip(self.request)
        user_id = None
        context['product_gallery_group'] = grouped(
            list(ProductGallery.objects.filter(products_id=loaded_product.id).all()), 3)
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
        has_been_visited = ProductVisited.objects.filter(ip__iexact=user_ip, product_id=loaded_product.id).exists()
        if not has_been_visited:
            new_visit = ProductVisited(ip=user_ip, user_id=user_id, product_id=loaded_product.id)
            new_visit.save()
        color_prices = {}
        base_price = loaded_product.price
        for color in loaded_product.colors.all():
            price_by_color = PriceByProductColor.objects.filter(products=loaded_product, colors=color).first()
            if price_by_color:
                color_prices[color.id] = price_by_color.price_by_color
            else:
                color_prices[color.id] = base_price

        context['suggestion'] = Products.objects.filter(suggest__products=loaded_product,
                                                        car_products=loaded_product.car_products).exclude(
            id=loaded_product.id).distinct()

        context['color_prices'] = color_prices
        product: Products = kwargs.get('object')
        context['comments'] = ProductComment.objects.filter(product_id=product.id, parent=None,
                                                            is_active=True).prefetch_related(
            Prefetch('productcomment_set', queryset=ProductComment.objects.filter(is_active=True)))
        context['comments_count'] = ProductComment.objects.filter(product_id=product.id, is_active=True).count()
        return context


def cars_include(request):
    cars = ProductCars.objects.filter(is_active=True, car_id=None).all()
    context = {'cars': cars}
    return render(request, 'categories/includs/cars.html', context)


def brands_include(request):
    brands = Product_Brand.objects.filter(is_active=True).all()
    context = {'brands': brands}
    return render(request, 'categories/includs/brands.html', context)


def omdeh(request):
    return render(request, 'omdeh.html')


def ProductCategories(request):
    categories = Product_Category.objects.filter(is_active=True, category_id=None).all()
    context = {'categories': categories,
               }
    return render(request, 'categories/categories.html', context)


def ProductCategoryComponent(request):
    categories = Product_Category.objects.prefetch_related('product_category_set').filter(is_active=True,
                                                                                          category_id=None)
    context = {'categories': categories}
    return render(request, 'products/product-category-component.html', context)


def ProductBrandsComponent(request):
    brands = Product_Brand.objects.filter(is_active=True).annotate(product_count=Count('products'))
    context = {'brands': brands}
    return render(request, 'products/product-brands-component.html', context)


def ProductCarsComponent(request):
    cars = ProductCars.objects.prefetch_related('productcars_set').filter(is_active=True, car_id=None)
    context = {'cars': cars}
    return render(request, 'products/product-cars-component.html', context)


def products_filter_menu_component(request):
    return render(request, 'categories/includs/filters_menu/filters_menu.html')


def product_acces_componnetnt(request):
    categories = Product_Category.objects.filter(is_active=True, category_id=None).all()
    return render(request, 'includes/accsrs_to_products.html', {'categories': categories})


@csrf_exempt
def add_products_comment(request):
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            response = {
                'status': 'success',
                'message': 'نظر شما با موفقیت ثبت شد و پس از بازبینی منتشر خواهد شد'
            }
        else:
            response = {
                'status': 'error',
                'message': 'فرم معتبر نیست',
                'errors': form.errors.as_json()
            }
        return JsonResponse(response)
    else:
        return JsonResponse({'status': 'error', 'message': 'روش ارسال پشتیبانی نمی‌شود یا کاربر احراز هویت نشده است'})
