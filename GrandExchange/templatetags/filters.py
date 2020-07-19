from django import template
from datetime import date, datetime, timedelta

register = template.Library()


@register.filter
def slug(obj):
    return obj.getSlug()


@register.filter
def concat(str, arg):
    return str(str) + str(arg)


@register.filter
def get_time(str, format):
    date = datetime.strptime(str, "%Y-%m-%d")
    return "test"

