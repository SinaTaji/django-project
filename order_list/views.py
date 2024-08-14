import json
from Lib.django.contrib.auth.decorators import login_required
from Lib.django.http.request import HttpRequest
from Lib.django.http.response import JsonResponse
from Lib.django.shortcuts import redirect
from datetime import datetime
import requests
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from order_list.models import Order, OrderDetail
from products.models import Products, Product_color

if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"
CallbackURL = 'http://localhost:8000/order/verify/'


def add_order_list(request: HttpRequest):
    product_id = request.GET.get('products_id')
    count = int(request.GET.get('count'))
    color_id = request.GET.get('color_id')
    side = request.GET.get('side')
    session_id = request.session.session_key

    if not session_id:
        request.session.create()
        session_id = request.session.session_key
    if count < 1:
        return JsonResponse({
            'status': 'invalid_count',
            'text': 'مقدار وارد شده صحیح نمیباشد !',
            'icon': 'error',
            'confirmButtonText': 'ممنون'
        })

    product = Products.objects.filter(id=product_id, is_active=True).first()

    if product:
        if request.user.is_authenticated:
            current_order, created = Order.objects.get_or_create(is_paid=False, user=request.user)
        else:
            current_order, created = Order.objects.get_or_create(is_paid=False, session=session_id)

        if not product.has_color:
            current_order_detail = current_order.orderdetail_set.filter(products_id=product_id, side=side).first()
            if current_order_detail:
                current_order_detail.count += int(count)
                current_order_detail.save()
            else:
                new_detail = OrderDetail(products_id=product_id, order_id=current_order.id, count=count, side=side)
                new_detail.save()

            return JsonResponse({
                'status': 'success-add',
                'text': 'محصول شما با موفقیت به سبد خرید اضافه شد',
                'icon': 'success',
                'confirmButtonText': 'مشاهده سبد خرید',
                'cancelButtonText': 'ادامه خرید'
            })
        if color_id and color_id != 'default':
            color = Product_color.objects.filter(id=color_id).first()
            if color:
                current_order_detail = current_order.orderdetail_set.filter(
                    products_id=product_id,
                    products_color_id=color.id,
                    side=side
                ).first()
                if current_order_detail:
                    current_order_detail.count += int(count)
                    current_order_detail.save()
                else:
                    new_detail = OrderDetail(
                        products_id=product_id,
                        products_color_id=color.id,
                        order_id=current_order.id,
                        count=count,
                        side=side
                    )
                    new_detail.save()

                return JsonResponse({
                    'status': 'success-add',
                    'text': 'محصول شما با موفقیت به سبد خرید اضافه شد',
                    'icon': 'success',
                    'confirmButtonText': 'مشاهده سبد خرید',
                    'cancelButtonText': 'ادامه خرید'
                })
            else:
                return JsonResponse({
                    'status': 'warning',
                    'text': 'رنگ مورد نظر یافت نشد!',
                    'icon': 'warning',
                    'confirmButtonText': 'ممنون'
                })
    return JsonResponse({
        'status': 'warning',
        'text': 'محصول مورد نظر یافت نشد!',
        'icon': 'warning',
        'confirmButtonText': 'ممنون'
    })


@login_required
def send_request(request):
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_price = current_order.calculate_total()
    if total_price == 0:
        return redirect(reverse('user_basket_page'))
    data = {
        "MerchantID": settings.MERCHANT,
        "currency": "IRT",
        "Amount": float(total_price),
        "Description": description,
        "CallbackURL": CallbackURL,
        # "Phone": phone,
        # "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                return redirect(ZP_API_STARTPAY + str(response['Authority']))
            else:
                return {'status': False, 'code': str(response['Status'])}
        return JsonResponse(response)

    except requests.exceptions.Timeout:
        return JsonResponse({'status': False, 'code': 'timeout'})
    except requests.exceptions.ConnectionError:
        return JsonResponse({'status': False, 'code': 'connection error'})


@login_required
def verify(request: HttpRequest):
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_price = current_order.calculate_total()
    authority = request.GET.get('Authority', '')
    status = request.GET.get('Status', '')

    data = {
        "MerchantID": settings.MERCHANT,
        "currency": "IRT",
        "Amount": float(total_price),
        "Authority": authority,
    }

    data_json = json.dumps(data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data_json))}

    try:
        response = requests.post(ZP_API_VERIFY, data=data_json, headers=headers)
        response_data = response.json()
        if status == 'OK':
            if 'errors' not in response_data:
                if response_data['RefID'] != 0:
                    t_status = response_data['Status']
                    if t_status == 100:
                        current_order.is_paid = True
                        current_order.payment_date = datetime.now()
                        current_order.final_price = total_price
                        current_order.save()
                        context = {
                            'success': True,
                            'current_order': current_order,
                            'ref_str': response_data['RefID'],
                            'user': request.user
                        }

                        return render(request, 'order_module/payment_result.html', context)
                    elif t_status == 101:
                        return render(request, 'order_module/payment_result.html', {
                            'info': 'این تراکنش قبلا ثبت شده است'
                        })
                    else:
                        return render(request, 'order_module/payment_result.html', {
                            'error': "در دسترس نیست"
                        })
                else:
                    return render(request, 'order_module/payment_result.html', {
                        'error': 'ساختار پاسخ دریافتی نامشخص است'
                    })
            else:
                e_code = response_data['errors'].get('code', 'نامشخص')
                e_message = response_data['errors'].get('message', 'پیام خطا در دسترس نیست')
                return render(request, 'order_module/payment_result.html', {
                    'error': f'کد خطا: {e_code}, پیام خطا: {e_message}'
                })
        else:
            return render(request, 'order_module/payment_result.html', {
                'error': 'error'
            })
    except requests.exceptions.RequestException as e:
        return render(request, 'order_module/payment_result.html', {
            'error': f'خطای درخواست: {str(e)}'
        })
