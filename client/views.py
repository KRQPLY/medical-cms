from django.shortcuts import render
from .models import Slider


def home_view(request):
    slider = Slider.objects.get(name="Slider Main")

    slider_items = slider.slideritem_set.all()

    return render(request, 'index.html', {'slides': slider_items})


def error_view(request):
    return render(request, '404.html')


def blog_view(request):
    return render(request, 'blog-single.html')


def contact_view(request):
    return render(request, 'contact.html')


def portfolio_view(request):
    return render(request, 'portfolio-details.html')
