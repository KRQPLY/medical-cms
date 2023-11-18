from django.shortcuts import render
from .models import Page


def home_view(request):
    page, _ = Page.objects.get_or_create(name="Main Page")

    components = page.get_components()

    return render(request, 'index.html', {'components': components})


def error_view(request):
    return render(request, '404.html')


def blog_view(request):
    return render(request, 'blog-single.html')


def contact_view(request):
    return render(request, 'contact.html')


def portfolio_view(request):
    return render(request, 'portfolio-details.html')
