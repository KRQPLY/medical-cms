from django.contrib import admin
from .models import Slider, SliderItem, Schedule, ScheduleItem, Feature, FeatureItem, Page, Facts, FactsItem, Video, VideoItem

admin.site.register(Page)

admin.site.register(Slider)
admin.site.register(SliderItem)
admin.site.register(Schedule)
admin.site.register(ScheduleItem)
admin.site.register(Feature)
admin.site.register(FeatureItem)
admin.site.register(Facts)
admin.site.register(FactsItem)
admin.site.register(Video)
admin.site.register(VideoItem)
