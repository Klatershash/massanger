from django import template
register =template.Library()


@register.filter(name='str_text')
def str_text(value):
    return str(value)