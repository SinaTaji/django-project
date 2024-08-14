from django.contrib.auth import login, logout
from django.http import HttpRequest, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from User.forms import RegisterUserForm, LogInUserForm, ResetPassForm, ForgotPassForm
from order_list.models import Order
from .models import User
from django.utils.crypto import get_random_string
from utils.email_service import send_email
from django.contrib import messages


class RegisterUserView(View):
    def get(self, request: HttpRequest):
        register_form = RegisterUserForm()
        context = {'register_form': register_form}
        return render(request, 'User/register_user.html', context)

    def post(self, request: HttpRequest):
        register_form = RegisterUserForm(request.POST)
        if register_form.is_valid():
            user_name = register_form.cleaned_data.get('user_name')
            email = register_form.cleaned_data.get('email')
            password = register_form.cleaned_data.get('password')
            user: bool = User.objects.filter(email__iexact=email).exists()
            if user:
                register_form.add_error('email', 'این ایمیل قبلا ثبت نام شده است')
            else:
                new_user = User(
                    username=user_name,
                    email=email,
                    email_active_code=get_random_string(72),
                    is_active=False)
                new_user.set_password(password)
                new_user.save()
                message = 'ایمیل حاوی لینک فعالسازی با موفقیت برای شما ارسال شد!'
                send_email('فعالسازی حساب کاربری', new_user.email, {'user': new_user}, 'emails/activate_account.html')
                messages.success(request,
                                 'ثبت نام با موفقیت انجام شد ایمیل حاوی لینک فعال سازی حساب شما ارسال شد لطفا ایمیل خود را چک کنید')
                return render(request, 'User/register_user.html', {'register_form': register_form, 'message': message})

        context = {'register_form': register_form,
                   }
        return render(request, 'User/register_user.html', context)


class ActiveUserView(View):
    def get(self, request: HttpRequest, email_active_code):
        user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user:
            if not user.is_active:
                user.is_active = True
                user.email_active_code = get_random_string(72)
                user.save()
                return redirect(reverse('login_page'))
            else:
                pass
        raise Http404


class LoginUserView(View):
    def get(self, request: HttpRequest):
        login_form = LogInUserForm()
        next_url = request.GET.get('next', reverse('home_page'))
        context = {'login_form': login_form, 'next': next_url}
        return render(request, "User/login_user.html", context)

    def post(self, request: HttpRequest):
        login_form = LogInUserForm(request.POST)
        if login_form.is_valid():
            next_url = request.POST.get('next', reverse('home_page'))
            user_email = login_form.cleaned_data.get('email')
            user_password = login_form.cleaned_data.get('password')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user:
                if not user.is_active:
                    login_form.add_error('email', 'حساب شما فعال نشده است ')
                else:
                    is_password_correct = user.check_password(user_password)
                    if is_password_correct:
                        session_key = request.session.session_key
                        if not session_key:
                            request.session.create()
                            session_key = request.session.session_key

                        session_order = Order.objects.filter(is_paid=False, session=session_key).first()
                        if session_order:
                            if request.user.is_authenticated:
                                user_order, created = Order.objects.get_or_create(
                                    is_paid=False, user_id=request.user.id)

                                for detail in session_order.orderdetail_set.all():
                                    existing_detail = user_order.orderdetail_set.filter(
                                        products_id=detail.products_id,
                                        side=detail.side,
                                        products_color_id=detail.products_color_id
                                    ).first()
                                    if existing_detail:
                                        existing_detail.count += detail.count
                                        existing_detail.save()
                                    else:
                                        detail.order = user_order
                                        detail.session = None
                                        detail.save()

                                session_order.delete()
                            else:

                                user_order, created = Order.objects.get_or_create(
                                    is_paid=False, user=user)

                                for detail in session_order.orderdetail_set.all():
                                    existing_detail = user_order.orderdetail_set.filter(
                                        products_id=detail.products_id,
                                        side=detail.side,
                                        products_color_id=detail.products_color_id
                                    ).first()
                                    if existing_detail:
                                        existing_detail.count += detail.count
                                        existing_detail.save()
                                    else:
                                        detail.order = user_order
                                        detail.session = None
                                        detail.save()

                                session_order.delete()
                        login(request, user)
                        return redirect(next_url)
                    else:
                        login_form.add_error('email', "کلمه عبور یا ایمیل شما اشتباه است ")
            else:
                login_form.add_error('email', ' این ایمیل یافت نشد')
        context = {'login_form': login_form}
        return render(request, "User/login_user.html", context)


class LogOutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('home_page'))


class ForgotPasswordView(View):
    def get(self, request: HttpRequest):
        forgot_pass = ForgotPassForm()
        context = {'forgot_pass': forgot_pass}
        return render(request, 'User/forgot_pass.html', context)

    def post(self, request: HttpRequest):
        forgot_pass = ForgotPassForm(request.POST)
        if forgot_pass.is_valid():
            email = forgot_pass.cleaned_data.get('email')
            user: User = User.objects.filter(email__iexact=email).first()
            if user:
                user.email_active_code = get_random_string(72)
                user.save()
                send_email('فراموشی کلمه عبور', user.email, {'user': user}, 'emails/forgot_pass_email.html')
                messages.success(request,
                                 "ایمیل حاوی لینک بازیابی کلمه عبور با موفقیت برای شما ارسال گردید لطفا ایمل خود را چک کنید!")
            else:
                forgot_pass.add_error('email', 'ایمیل وارد شده اشتباه است یا موجود نیست')
        context = {'forgot_pass': forgot_pass,
                   }
        return render(request, 'User/forgot_pass.html', context)


class ResetPasswordView(View):
    def get(self, request: HttpRequest, active_code):
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if user is None:
            return redirect(reverse('login_page'))

        reset_pass = ResetPassForm()

        context = {
            'reset_pass_form': reset_pass,
            'user': user
        }
        return render(request, 'User/reset_pass.html', context)

    def post(self, request: HttpRequest, active_code):
        reset_pass_form = ResetPassForm(request.POST)
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if reset_pass_form.is_valid():
            if user is None:
                return redirect(reverse('login_page'))
            user_new_pass = reset_pass_form.cleaned_data.get('password')
            user.set_password(user_new_pass)
            user.email_active_code = get_random_string(72)
            user.is_active = True
            user.save()
            return redirect(reverse('login_page'))

        context = {
            'reset_pass_form': reset_pass_form,
            'user': user
        }

        return render(request, 'User/reset_pass.html', context)
