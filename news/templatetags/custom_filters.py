from django import template
from django.template.defaultfilters import date

register = template.Library()


@register.filter
def format_time(value, format_string='d.m.Y'):
    return date(value, format_string)


censored_words = ['shit', 'fucking', 'fuck', 'damn', 'shitty']


@register.filter()
def censor(value):
    censored_value = value
    for word in censored_words:
        if len(word) > 1:
            replacement = word[0] + '*' * (len(word) - 1)
            censored_value = censored_value.replace(word.lower(), replacement.lower(), 1)
            censored_value = censored_value.replace(word.capitalize(), replacement.capitalize(), 1)
            censored_value = censored_value.replace(word.upper(), replacement.upper(), 1)
    return censored_value
