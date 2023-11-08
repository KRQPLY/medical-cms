from django.shortcuts import render
from .models import Slider, Schedule, Feature


def home_view(request):
    slider, _ = Slider.objects.get_or_create(name="Slider Main")
    schedule, _ = Schedule.objects.get_or_create(name="Schedule")
    feature, _ = Feature.objects.get_or_create(name="Feature")
    # funFacts, _ = FunFacts.objects.get_or_create(name="FunFacts")

    slider_items = slider.slideritem_set.all()
    schedule_items = schedule.scheduleitem_set.all()
    feature_items = feature.featureitem_set.all()
    # funFacts_items = funFacts.funfactsitem_set.all()

    return render(request, 'index.html', {'slides': slider_items, 'schedules': schedule_items, 'feature':feature_items})


def error_view(request):
    return render(request, '404.html')


def blog_view(request):
    return render(request, 'blog-single.html')


def contact_view(request):
    return render(request, 'contact.html')


def portfolio_view(request):
    return render(request, 'portfolio-details.html')
