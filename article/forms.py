from django import forms
from .models import ArticleComment


class CommentForm(forms.ModelForm):
    class Meta:
        model = ArticleComment
        fields = ['text', 'article', 'parent']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
            'article': forms.HiddenInput(),
            'parent': forms.HiddenInput()
        }
        labels = {
            'text': 'متن نظر',
            'article': 'مقاله',
            'parent': 'کامنت والد'
        }
        error_messages = {
            'text': {
                'required': 'متن پیام شما نباید خالی باشد'
            }
        }
