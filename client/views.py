from django.shortcuts import render
from .models import Slider, Schedule


def home_view(request):
    slider = Slider.objects.get(name="Slider Main")
    schedule = Schedule.objects.get(name="Schedule")

    slider_items = slider.slideritem_set.all()
    schedule_items = schedule.scheduleitem_set.all()

    return render(request, 'index.html', {'slides': slider_items, 'schedules': schedule_items})


def error_view(request):
    return render(request, '404.html')


def blog_view(request):
    return render(request, 'blog-single.html')


def contact_view(request):
    return render(request, 'contact.html')


def portfolio_view(request):
    return render(request, 'portfolio-details.html')
