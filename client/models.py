from django.db import models
from django.apps import apps


class Component:
    isComponent = True

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
        return True


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
    description = models.TextField()
    left_button = models.CharField(max_length=200)
    right_button = models.CharField(max_length=200)
    background = models.ImageField(upload_to='slider/%Y/%m/%d')
    slider = models.ForeignKey(Slider, on_delete=models.CASCADE)

    def __str__(self):
        return self.heading


class Schedule(models.Model, Component, Model):
    name = models.CharField(max_length=100)
    childModel = 'ScheduleItem'

    def is_safe_to_add_new(self):
        return self.scheduleitem_set.count() < 3

    def __str__(self):
        return self.name


class ScheduleItem(models.Model, Model):
    title = models.TextField()
    heading = models.TextField()
    description = models.TextField()
    button = models.CharField(max_length=200)
    icon = models.CharField(max_length=200)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    def __str__(self):
        return self.heading
