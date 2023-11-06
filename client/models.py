from django.db import models
from django.apps import apps
from ckeditor.fields import RichTextField


class Component:
    isComponent = True
    maxItems = 0
    isActive = models.BooleanField(default=True)

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


class Feaute(models.Model, Component, Model):
    name = models.CharField(max_length=100)
    childModel = 'FeauteItem'
    maxItems = 1

    def __str__(self):
        return self.name
    
    
class FeauteItem(models.Model, Model):
    heading = models.TextField()
    description = RichTextField()
    feaute= models.ForeignKey(Feaute, on_delete=models.CASCADE)

    def __str__(self):
        return self.heading