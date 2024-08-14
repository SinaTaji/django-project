from Lib.django.db.models.aggregates import Count
from Lib.django.views.generic.base import TemplateView
from site_setting.models import Link_Boxes, SiteSettings
from products.models import ProductCars, Products, ProductGallery, Product_Category
from django.shortcuts import render
from utils.convertor import grouped
from .forms import SearchForm


class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cars = ProductCars.objects.filter(car__isnull=False)
        context['cars'] = cars

        latest_products = Products.objects.filter(is_active=True).order_by('-id')[:18]
        context['latest_products'] = latest_products

        most_visited_products = Products.objects.filter(is_active=True).annotate(
            visit_count=Count('productvisited')).order_by('-visit_count')[:18]
        context['most_visited_products'] = most_visited_products
        context['categories'] = Product_Category.objects.prefetch_related('product_category_set').filter(is_active=True,
                                                                                                         category_id=None)
        context['product_categories'] = Products.objects.prefetch_related('Category').filter(is_active=True).all()
        return context


def searchbox_component(request):
    form = SearchForm()
    return render(request, 'shared/searchbox/search_box.html', {'form': form})


def searchbox_resualt(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        search = form.cleaned_data['search']
        products = Products.objects.all().filter(title__icontains=search)
    return render(request, 'shared/searchbox/search_box_resualt.html',
                  {'form': form, 'products': products, 'search': search})


def footer_component(request):
    link_boxes = Link_Boxes.objects.all()
    site_settings = SiteSettings.objects.filter(is_active=True).first()
    context = {
        'link_boxes': link_boxes,
        'site_settings': site_settings,
    }
    return render(request, 'shared/footer_component.html', context)


def header_component(request):
    form = SearchForm()
    return render(request, "shared/header_component.html", {'form': form})
