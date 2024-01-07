from django import template
import math 

register = template.Library()


@register.filter
def get_attribute(item, attr_name):
    try:
        return getattr(item, attr_name)
    except AttributeError:
        return None

@register.filter
def parse_page_name(page):
    return page.name.replace('-', ' ')

@register.filter
def array_in_half(array, index):
    mid_id = math.ceil(len(array)/2)
    
    return [array[:mid_id], array[mid_id:]][index]
