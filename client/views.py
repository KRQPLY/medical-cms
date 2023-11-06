from django.shortcuts import render
from .models import Slider, Schedule, Feaute


def home_view(request):
    slider, _ = Slider.objects.get_or_create(name="Slider Main")
    schedule, _ = Schedule.objects.get_or_create(name="Schedule")
    feaute, _ = Feaute.objects.get_or_create(name="Feaute")

    slider_items = slider.slideritem_set.all()
    schedule_items = schedule.scheduleitem_set.all()
    feautes_items = feaute.feauteitem_set.all()

    return render(request, 'index.html', {'slides': slider_items, 'schedules': schedule_items, 'feautes':feautes_items})


def error_view(request):
    return render(request, '404.html')


def blog_view(request):
    return render(request, 'blog-single.html')


def contact_view(request):
    return render(request, 'contact.html')


def portfolio_view(request):
    return render(request, 'portfolio-details.html')
