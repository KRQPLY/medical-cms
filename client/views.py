from django.shortcuts import render
from .models import Page
from .helpers.get_main_pages import get_main_pages

def page_view(request, page_name='home'):
    # TODO browse throught main pages | pass pages to the header and footer components
    print(get_main_pages())
    try:
        page = Page.objects.get(name=page_name)

        components = page.get_components()

        return render(request, page.template, {'components': components})
    except Page.DoesNotExist:
        return render(request, '404.html')

