from django import template
from babel.numbers import format_currency

register = template.Library()

@register.filter
def rupiah_format(value):
    try:
        value = float(value)
        return format_currency(value, 'IDR', locale='id_ID')
    except (ValueError, TypeError):
        return value
