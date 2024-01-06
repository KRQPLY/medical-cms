from ..models import Page

def get_main_pages():
    all_pages = Page.objects.all()
    return list(filter(lambda page: page.parent == None, all_pages))