from django.db import models
from django.apps import apps
from ckeditor.fields import RichTextField


class Page(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Component:
    isComponent = True
    maxItems = 0
    isActive = models.BooleanField(default=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)

    def get_children(self):
        return getattr(self, self.childModel.lower() + '_set').all()

    def get_children_fields(self):
        model_class = apps.get_model(
            app_label='client', model_name=self.childModel)
        if model_class:
            return model_class._meta.get_fields()
        else:
            return []
        
    def is_safe_to_add_new(self):
        return self.maxItems == 0 or getattr(self, self.childModel.lower() + '_set').count() < self.maxItems



class Model:
    def class_name(self):
        return self.__class__.__name__

    def get_fields(self):
        return self._meta.get_fields()


class Slider(models.Model, Component, Model):
    name = models.CharField(max_length=100)
    childModel = 'SliderItem'

    def __str__(self):
        return self.name


class SliderItem(models.Model, Model):
    heading = models.TextField()
    description = RichTextField()
    left_button = models.CharField(max_length=200)
    right_button = models.CharField(max_length=200)
    background = models.ImageField(upload_to='slider/%Y/%m/%d')
    slider = models.ForeignKey(Slider, on_delete=models.CASCADE)

    def __str__(self):
        return self.heading


class Schedule(models.Model, Component, Model):
    name = models.CharField(max_length=100)
    childModel = 'ScheduleItem'
    maxItems = 3

    def __str__(self):
        return self.name


class ScheduleItem(models.Model, Model):
    title = models.TextField()
    heading = models.TextField()
    description = RichTextField()
    button = models.CharField(max_length=200)
    icon = models.CharField(max_length=200)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    def __str__(self):
        return self.heading


class Feature(models.Model, Component, Model):
    name = models.CharField(max_length=100)
    childModel = 'FeatureItem'
    maxItems = 1

    def __str__(self):
        return self.name
    
    
class FeatureItem(models.Model, Model):
    heading = models.TextField()
    description = RichTextField()
    feature= models.ForeignKey(Feature, on_delete=models.CASCADE)

    def __str__(self):
        return self.heading
    
# class FunFacts(models.Model, Component, Model):
#     name = models.CharField(max_length=100)
#     childModel = 'FunFactsItem'
#     maxItems = 4

#     def __str__(self):
#         return self.name
    
# class FunFactsItem(models.Model, Model):
#     icon = models.CharField(max_length=200)
#     counter = models.FloatField()
#     content = RichTextField()
#     funFacts = models.ForeignKey(FunFacts, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.content