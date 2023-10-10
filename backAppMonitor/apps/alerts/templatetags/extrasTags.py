from django import template

register = template.Library()

@register.filter
def comaBydot(value):
    return str(value).replace(",", ".")