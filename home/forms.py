from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(
        max_length=100, label='',
        widget=forms.TextInput(attrs={'placeholder': 'جست و جو'})
    )
