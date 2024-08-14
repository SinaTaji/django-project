from products.models import ProductComment
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = ['text', 'product', 'parent']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
            'product': forms.HiddenInput(),
            'parent': forms.HiddenInput()
        }
        labels = {
            'text': 'متن نظر',
            'product': 'محصول',
            'parent': 'کامنت والد'
        }
        error_messages = {
            'text': {
                'required': 'متن پیام شما نباید خالی باشد'
            }
        }




