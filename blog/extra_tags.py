from django import template
from . import views

register = template.Library()


@register.simple_tag()
def weather():
    return views.weather()
