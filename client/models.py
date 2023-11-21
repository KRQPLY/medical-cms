from django.db import models
from django.apps import apps
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

class Model:
    def class_name(self):
        return self.__class__.__name__

    def get_fields(self):
        return self._meta.get_fields()

class Page(models.Model, Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='created_pages')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='modified_pages')

    def get_components(self):
        fields = self._meta.related_objects
        components = []
        for field in fields:
            if getattr(self, field.name.lower() + '_set').exists():
                related_set = getattr(self, field.get_accessor_name())
                components.extend(related_set.all())

        components.sort(key=lambda x: x.order)
 
        return components
    
    def __str__(self):
        return self.name

class Component(models.Model):
    isComponent = True
    maxItems = 0
    order = models.PositiveIntegerField(default=0)
    isActive = models.BooleanField(default=True, choices=((True, 'TRUE'), (False, 'FALSE')))
    #page = models.ForeignKey(Page, on_delete=models.SET_NULL, blank=True, null=True)
    page = models.ManyToManyField(Page, blank=True)
    class Meta:
        abstract = True

    def get_children(self):
        return getattr(self, self.childModel.lower() + '_set').all().order_by('order')

    def get_children_fields(self):
        model_class = apps.get_model(
            app_label='client', model_name=self.childModel)
        if model_class:
            return model_class._meta.get_fields()
        else:
            return []
        
    def is_safe_to_add_new(self):
        return self.maxItems == 0 or getattr(self, self.childModel.lower() + '_set').count() < self.maxItems
    
class Item(models.Model):
    isItem = True
    order = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True

class Slider(Component, Model):
    name = models.CharField(max_length=100)
    childModel = 'SliderItem'

    def __str__(self):
        return self.name


class SliderItem(Item, Model):
    heading = models.TextField()
    description = RichTextField()
    left_button = models.CharField(max_length=200)
    right_button = models.CharField(max_length=200)
    background = models.ImageField(upload_to='slider/%Y/%m/%d')
    slider = models.ForeignKey(Slider, on_delete=models.CASCADE)

    def __str__(self):
        return self.heading


class Schedule(Component, Model):
    name = models.CharField(max_length=100)
    childModel = 'ScheduleItem'
    maxItems = 3

    def __str__(self):
        return self.name


class ScheduleItem(Item, Model):
    title = models.TextField()
    heading = models.TextField()
    description = RichTextField()
    button = models.CharField(max_length=200)
    icon = models.CharField(max_length=200)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    def __str__(self):
        return self.heading


class Feature(Component, Model):
    name = models.CharField(max_length=100)
    childModel = 'FeatureItem'
    maxItems = 1

    def __str__(self):
        return self.name
    
    
class FeatureItem(Item, Model):
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