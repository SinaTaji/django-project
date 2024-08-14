from django import forms
from .models import ContactUsModel


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUsModel
        fields = ['title', 'full_name', 'email', 'message']

        widgets = {
            "full_name": forms.TextInput(attrs={
                'class': 'form-control'
            }),

            "email": forms.EmailInput(attrs={
                'class': 'form-control'
            }),

            "title": forms.TextInput(attrs={
                'class': 'form-control'
            }),

            "message": forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'message',
            }),
        }
        labels = {
            'full_name': 'نام و نام خانوادگی شما',
            'email': 'ایمیل شما'
        }

        error_messages = {
            'full_name': {
                'required': 'نام و نام خانوادگی اجباری می باشد. لطفا وارد کنید'
            }
        }