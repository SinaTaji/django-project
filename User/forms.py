from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from .models import User


class RegisterUserForm(forms.Form):
    user_name = forms.CharField(
        label='نام کاربری',
        widget=forms.TextInput(attrs={'class': 'inp',
                                          'placeholder': 'نام کاربری'}),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={'class': 'inp',
                                          'placeholder': 'ایمیل'}),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator()
        ]
    )
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(attrs={'class': 'inp',
                                          'placeholder': ' کلمه عبور'}),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    confirm_password = forms.CharField(
        label='تکرار کلمه عبور',
        widget=forms.PasswordInput(attrs={'class': 'inp',
                                          'placeholder': 'تکرار کلمه عبور'}),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if confirm_password == password:
            return confirm_password
        raise ValidationError('تکرار کلمه عبور شما با کلمه عبور شما مغایرت دارد')

    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        if User.objects.filter(username=user_name).exists():
            raise ValidationError('این نام کاربری قبلا استفاده شده است')
        return user_name


class LogInUserForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',

        widget=forms.EmailInput(attrs={'class': 'inp',
                                       'placeholder': 'ایمیل شما'}),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator()
        ]
    )
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(attrs={'class': 'inp',
                                       'placeholder': ' کلمه عبور'}),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )


class ForgotPassForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={'class': 'inp',
                                       'placeholder': 'ایمیل شما'}),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator()
        ]
    )


class ResetPassForm(forms.Form):
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(attrs={'class': 'inp',
                                          'placeholder': ' کلمه عبور جدید'}),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    confirm_password = forms.CharField(
        label='تکرار کلمه عبور',
        widget=forms.PasswordInput(attrs={'class': 'inp',
                                          'placeholder': 'تکرار کلمه عبور'}),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if confirm_password == password:
            return confirm_password
        raise ValidationError('تکرار کلمه عبور شما با کلمه عبور شما مغایرت دارد')
