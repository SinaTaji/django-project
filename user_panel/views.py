from Lib.django.contrib.auth import logout
from Lib.django.http.request import HttpRequest
from Lib.django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from User.models import User
from order_list.models import Order, OrderDetail, final_payment
from products.models import PriceByProductColor
from .forms import ChangeUserInformationForm, user_change_passwordForm, final_payment_Form


@login_required
def user_panel_mennu_component(request):
    current_user = User.objects.filter(id=request.user.id).first()
    form = ChangeUserInformationForm(instance=current_user)
    context = {'form': form,
               }
    return render(request, 'user_panel/component/dashboard_menu.html', context)


@method_decorator(login_required, name='dispatch')
class user_change_informations(View):
    template_name = 'user_panel/user_change_informations.html'

    def get(self, request):
        current_user = User.objects.filter(id=request.user.id).first()
        form = ChangeUserInformationForm(instance=current_user)
        context = {'form': form,
                   'current_user': current_user, }
        return render(request, 'user_panel/user_change_informations.html', context)

    def post(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        form = ChangeUserInformationForm(request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            form.save(commit=True)
        context = {'form': form,
                   'current_user': current_user}
        return render(request, 'user_panel/user_change_informations.html', context)


@method_decorator(login_required, name='dispatch')
class change_user_password(View):
    template_name = 'user_panel/change_user_password.html'

    def get(self, request):
        context = {'change_user_password': user_change_passwordForm()}
        return render(request, 'user_panel/change_user_password.html', context)

    def post(self, request):
        change_user_password = user_change_passwordForm(request.POST)
        if change_user_password.is_valid():
            current_user: User = User.objects.filter(id=request.user.id).first()
            if current_user.check_password(change_user_password.cleaned_data.get('current_password')):
                current_user.set_password(change_user_password.cleaned_data.get('password'))
                current_user.save()
                logout(request)
                return redirect(reverse('login_page'))
            else:
                change_user_password.add_error('password', 'کلمه عبور وارد شده صحیح نیست!')
        context = {
            'change_user_password': change_user_password
        }
        return render(request, 'user_panel/change_user_password.html', context)


@login_required
def user_dashboard(request):
    current_user = User.objects.filter(id=request.user.id).first()
    form = ChangeUserInformationForm(instance=current_user)
    context = {'form': form,
               'current_user': current_user}

    return render(request, 'user_panel/user_dashboard.html', context)


def user_basket(request):
    if request.user.is_authenticated:
        current_order, created = Order.objects.get_or_create(
            is_paid=False, user_id=request.user.id)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        current_order, created = Order.objects.get_or_create(
            is_paid=False, session=session_key)

    current_order = Order.objects.prefetch_related('orderdetail_set__products_color').get(id=current_order.id)

    total_price = 0
    order_details = []
    for order_detail in current_order.orderdetail_set.all():
        price_by_color = PriceByProductColor.objects.filter(
            products_id=order_detail.products_id,
            colors=order_detail.products_color
        ).first()
        color = order_detail.products_color
        if price_by_color:
            price = price_by_color.price_by_color
        else:
            price = order_detail.products.price

        order_total_price = price * order_detail.count
        total_price += order_total_price

        order_details.append({
            'color': color,
            'order': order_detail,
            'price': price,
            'order_total_price': order_total_price
        })

    context = {
        'current_order': current_order,
        'total_price': total_price,
        'order_details': order_details,
    }

    return render(request, 'user_basket/user_basket.html', context)


def user_basket_content(request):
    detail_id = request.GET.get('detail_id')

    if not detail_id:
        return JsonResponse({
            'status': 'not_found',
        })
    if request.user.is_authenticated:
        delete_count, delete_dict = OrderDetail.objects.filter(id=detail_id, order__is_paid=False,
                                                               order__user_id=request.user.id).delete()
    else:
        delete_count, delete_dict = OrderDetail.objects.filter(id=detail_id, order__is_paid=False,
                                                               order__session=request.session.session_key).delete()
    if delete_count == 0:
        return JsonResponse({
            'status': 'detail_not_found',
        })
    if request.user.is_authenticated:
        current_order, created = Order.objects.prefetch_related('orderdetail_set__products_color').get_or_create(
            is_paid=False, user_id=request.user.id)
    else:
        current_order, created = Order.objects.prefetch_related('orderdetail_set__products_color').get_or_create(
            is_paid=False, session=request.session.session_key)
    total_price = 0
    order_details = []
    for order_detail in current_order.orderdetail_set.all():

        price_by_color = PriceByProductColor.objects.filter(
            products_id=order_detail.products_id,
            colors=order_detail.products_color
        ).first()
        color = order_detail.products_color
        if price_by_color:
            price = price_by_color.price_by_color
        else:
            price = order_detail.products.price

        order_total_price = price * order_detail.count
        total_price += order_total_price

        order_details.append({
            'color': color,
            'order': order_detail,
            'price': price,
            'order_total_price': order_total_price
        })

    context = {
        'current_order': current_order,
        'total_price': total_price,
        'order_details': order_details,
    }
    data = render_to_string('user_basket/user_basket_content.html', context)
    return JsonResponse({
        'status': 'success',
        'data': data,
    })


def change_basket_content_count(request):
    detail_id = request.GET.get('detail_id')
    state = request.GET.get('state')
    if not detail_id or not state:
        return JsonResponse({
            'status': 'not_found',
        })
    if request.user.is_authenticated:
        order_detail = OrderDetail.objects.filter(id=detail_id, order__is_paid=False,
                                                  order__user_id=request.user.id).first()
    else:
        order_detail = OrderDetail.objects.filter(id=detail_id, order__is_paid=False,
                                                  order__session=request.session.session_key).first()
    if not order_detail:
        return JsonResponse({
            'status': 'order_detail_not_found',
        })
    if state == 'increase':
        order_detail.count += 1
        order_detail.save()
    elif state == 'decrease':
        if order_detail.count == 1:
            order_detail.delete()
        else:
            order_detail.count -= 1
            order_detail.save()
    else:
        return JsonResponse({
            'status': 'error',
        })
    if request.user.is_authenticated:
        current_order, created = Order.objects.prefetch_related('orderdetail_set__products_color').get_or_create(
            is_paid=False, user_id=request.user.id)
    else:
        current_order, created = Order.objects.prefetch_related('orderdetail_set__products_color').get_or_create(
            is_paid=False, session=request.session.session_key)
    total_price = 0
    order_details = []
    for order_detail in current_order.orderdetail_set.all():

        price_by_color = PriceByProductColor.objects.filter(
            products_id=order_detail.products_id,
            colors=order_detail.products_color
        ).first()
        color = order_detail.products_color
        if price_by_color:
            price = price_by_color.price_by_color
        else:
            price = order_detail.products.price

        order_total_price = price * order_detail.count
        total_price += order_total_price

        order_details.append({
            'color': color,
            'order': order_detail,
            'price': price,
            'order_total_price': order_total_price
        })

    context = {
        'current_order': current_order,
        'total_price': total_price,
        'order_details': order_details,
    }
    data = render_to_string('user_basket/user_basket_content.html', context)
    return JsonResponse({
        'status': 'success',
        'data': data,
    })


def way2pay(request):
    return render(request, 'payment/way2pay.html')


class finalPaymentForm_View(View):
    template_name = 'final_payment/final_payment.html'

    def get(self, request: HttpRequest):
        form = final_payment_Form()
        context = {
            'form': form,
        }

        return render(request, self.template_name, context)

    def post(self, request: HttpRequest):
        form = final_payment_Form(request.POST)
        if form.is_valid():
            final_pay = final_payment(
                order=Order.objects.filter(user_id=request.user.id).last(),
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                phone_number=form.cleaned_data['phone_number'],
                address=form.cleaned_data['address'],
                postal_code=form.cleaned_data['postal_code'],
                send_method=form.cleaned_data['send_method'],
            )
            final_pay.save()
            return redirect('request')
        return render(request, self.template_name, {'form': form})


def faktor_component(request: HttpRequest):
    if request.user.is_authenticated:
        current_order, created = Order.objects.get_or_create(
            is_paid=False, user_id=request.user.id)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        current_order, created = Order.objects.get_or_create(
            is_paid=False, session=session_key)

    current_order = Order.objects.prefetch_related('orderdetail_set__products_color').get(id=current_order.id)

    total_price = 0
    order_details = []
    for order_detail in current_order.orderdetail_set.all():
        price_by_color = PriceByProductColor.objects.filter(
            products_id=order_detail.products_id,
            colors=order_detail.products_color
        ).first()
        color = order_detail.products_color
        if price_by_color:
            price = price_by_color.price_by_color
        else:
            price = order_detail.products.price

        order_total_price = price * order_detail.count
        total_price += order_total_price

        order_details.append({
            'color': color,
            'order': order_detail,
            'price': price,
            'order_total_price': order_total_price
        })

    context = {
        'current_order': current_order,
        'total_price': total_price,
        'order_details': order_details,
    }

    return render(request, 'faktor/faktor_component.html', context)


def pay_card_to_card(request: HttpRequest):
    return render(request, 'payment/card_pay.html')
