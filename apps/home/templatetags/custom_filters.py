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
    def check_if_active(page):
        return page.show_in_footer
    
    active_items = list(filter(check_if_active, array))

    mid_id = math.ceil(len(active_items)/2)
    
    return [active_items[:mid_id], active_items[mid_id:]][index]

@register.filter
def get_active_subpages(page, component='header'):
    def check_if_active(page):
        if component == 'header':
            return page.show_in_header
        if component == 'footer':
            return page.show_in_footer
        
    subpages = page.get_all_subpages()
    active_subpages = list(filter(check_if_active, subpages))

    if(len(active_subpages)):
        return active_subpages
    else:
        return None