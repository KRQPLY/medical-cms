from django.shortcuts import render
from .helpers.get_main_pages import get_main_pages

def page_view(request, page_name='home', pages_names=''):
    main_pages = get_main_pages()
    called_page = None

    for page in main_pages:
        if page.name == page_name:
            called_page = page

    if not called_page:
        return render(request, '404.html', {'pages': main_pages})
    
    active_main_page = called_page

    if pages_names:
        paths = pages_names.split('/')

        for path in paths:
            subpage = called_page.get_subpage(path)

            if(not subpage):
                return render(request, '404.html', {'pages': main_pages})

            called_page = subpage

    components = called_page.get_components()

    return render(request, called_page.template, {'components': components, 'pages': main_pages, 'active_page': active_main_page})

