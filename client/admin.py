from django.contrib import admin
from .models import Slider, SliderItem, Schedule, ScheduleItem, Feature, FeatureItem, Page
#, FunFacts, FunFactsItem

admin.site.register(Page)

admin.site.register(Slider)
admin.site.register(SliderItem)
admin.site.register(Schedule)
admin.site.register(ScheduleItem)
admin.site.register(Feature)
admin.site.register(FeatureItem)
# admin.site.register(FunFacts)
# admin.site.register(FunFactsItem)
