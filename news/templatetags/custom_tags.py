from django import template
from datetime import datetime

register = template.Library()


@register.simple_tag()
def current_date(format_string='%d.%b.%Y'):
    return datetime.utcnow().strftime(format_string)
