from django import template

register = template.Library()


@register.filter
def get_attribute(item, attr_name):
    try:
        return getattr(item, attr_name)
    except AttributeError:
        return None

@register.filter
def parse_page_name(item):
    return item.name.replace('-', ' ')
