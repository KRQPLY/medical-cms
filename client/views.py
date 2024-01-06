from django.shortcuts import render
from .models import Page


def page_view(request, page_name='index.html'):
    try:
        page = Page.objects.get(name=page_name)

        components = page.get_components()

        return render(request, page.template, {'components': components})
    except Page.DoesNotExist:
        return render(request, '404.html')

