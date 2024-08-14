from User.models import User
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from order_list.models import final_payment

class ChangeUserInformationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'avatar', 'address', 'about_user']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control',
                                          'placeholder': 'نام'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control',
                                          'placeholder': ' نام خانوادگی'}),
            'username': forms.TextInput(attrs={'class': 'form-control',
                                          'placeholder': ' نام کاربری'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control',
                                          'placeholder': 'تصویر پروفایل'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                             'id': 'message',
                                          'placeholder': 'آدرس'}),
            'about_user': forms.Textarea(attrs={'class': 'form-control', 'rows': 6,
                                                'id': 'message',
                                          'placeholder': 'درباره شما'}),
        }
        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'avatar': 'تصویر پروفایل',
            'address': 'آدرس',
            'about_user': 'درباره شخص',
        }


class user_change_passwordForm(forms.Form):
    current_password = forms.CharField(
        label='کلمه عبور فعلی شما',
        widget=forms.PasswordInput(attrs={'class': 'inp',
                                          'placeholder': ' کلمه عبور فعلی'}),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    password = forms.CharField(
        label='کلمه عبور جدید',
        widget=forms.PasswordInput(attrs={'class': 'inp',
                                          'placeholder': ' کلمه عبور جدید'}),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    confirm_password = forms.CharField(
        label='تکرار کلمه عبور',
        widget=forms.PasswordInput(attrs={'class': 'inp',
                                          'placeholder': 'تکرار کلمه عبور جدید'}),
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



class final_payment_Form(forms.ModelForm):
    class Meta:
        model = final_payment
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control','placeholder':'استان شهرستان و محل تحویل', 'rows': 3}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2,}),
        }
