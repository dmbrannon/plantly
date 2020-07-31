from django import template
from django.template.defaultfilters import stringfilter
from datetime import date, datetime

register = template.Library()

@register.filter
@stringfilter
def upto(value, delimiter=None):
    return value.split(delimiter)[0]
upto.is_safe = True

@register.filter(expects_localtime=True)
def days_since(value, arg=None):
    try:
        tzinfo = getattr(value, 'tzinfo', None)
        value = date(value.year, value.month, value.day)
    except AttributeError:
        # Passed value wasn't a date object
        return value
    except ValueError:
        # Date arguments out of range
        return value
    today = datetime.now(tzinfo).date()
    delta = value - today
    if abs(delta.days) == 1:
        day_str = ("day")
    else:
        day_str = ("days")

    if delta.days < 1:
        fa_str = ("ago")
    else:
        fa_str = ("from now")

    return "%s %s %s" % (abs(delta.days), day_str, fa_str)