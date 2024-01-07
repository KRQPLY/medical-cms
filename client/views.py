from django.shortcuts import render
from .helpers.get_main_pages import get_main_pages

def page_view(request, page_name='home', pages_names=''):
    # TODO pass pages to the header and footer components
    main_pages = get_main_pages()
    called_page = None

    for page in main_pages:
        if page.name == page_name:
            called_page = page

    if not called_page:
        return render(request, '404.html')
    
    if not pages_names:
        components = called_page.get_components()

        return render(request, called_page.template, {'components': components})
    
    paths = pages_names.split('/')

    for path in paths:
        subpage = called_page.get_subpage(path)

        if(not subpage):
            return render(request, '404.html')

        called_page = subpage

    components = called_page.get_components()

    return render(request, called_page.template, {'components': components})

