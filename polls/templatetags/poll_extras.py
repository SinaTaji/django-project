from django import template
from jalali_date import date2jalali

register = template.Library()


@register.filter(name='date2jalali')
def date_2_jalali(value):
    return date2jalali(value)


@register.filter(name='int_comma')
def int_comma(value: int):
    return "{:,}".format(value) + " " + "تومان"


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)
