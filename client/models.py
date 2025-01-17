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
    TEMPLATE_CHOICES = (('index.html', 'Main Template'), ('blog-single.html', 'Blog Template'), ('contact.html', 'Contact Template'), ('portfolio-details.html', 'Portfolio Template'))

    name = models.CharField(max_length=100)
    show_in_header = models.BooleanField(default=True, choices=((True, 'TRUE'), (False, 'FALSE')))
    show_in_footer = models.BooleanField(default=True, choices=((True, 'TRUE'), (False, 'FALSE')))
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='created_pages')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='modified_pages')
    template = models.CharField(max_length=100, choices=TEMPLATE_CHOICES, default='index.html')

    def get_components(self):
        fields = self._meta.related_objects
        components = []
        for field in fields:
            if getattr(self, field.name.lower() + '_set').exists():
                related_set = getattr(self, field.get_accessor_name())
                if not issubclass(related_set.model, Page):
                    components.extend(related_set.all())

        components.sort(key=lambda x: x.order)
 
        return components
    
    def get_all_subpages(self):
        fields = self._meta.related_objects
        for field in fields:
            if field.name == 'page' and  getattr(self, field.name.lower() + '_set').exists():
                related_set = getattr(self, field.get_accessor_name())

                return related_set.all()
        return []
            
    def get_subpage(self, name):
        for subpage in self.get_all_subpages():
            if subpage.name == name:
                return subpage
        return None
    
    def __str__(self):
        return self.name

class Component(models.Model):
    isComponent = True
    maxItems = 0
    order = models.IntegerField(default=0)
    isActive = models.BooleanField(default=True, choices=((True, 'TRUE'), (False, 'FALSE')))
    #page = models.ForeignKey(Page, on_delete=models.SET_NULL, blank=True, null=True)
    page = models.ManyToManyField(Page, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='%(class)s_created_components')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='%(class)s_modified_components')

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
    order = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='%(class)s_created_items')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='%(class)s_modified_items')

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
    left_button_link = models.TextField()
    right_button_link = models.TextField()
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
    link = models.TextField()
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
    
class Facts(Component, Model):
    name = models.CharField(max_length=100)
    childModel = 'FactsItem'
    maxItems = 4

    def __str__(self):
        return self.name
    
class FactsItem(Item, Model):
    icon = models.CharField(max_length=200)
    counter = models.IntegerField(default=0)
    content = RichTextField()
    facts = models.ForeignKey(Facts, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
    
class Video(Component, Model):
    name = models.CharField(max_length=100)
    childModel = 'VideoItem'
    maxItems = 1

    def __str__(self):
        return self.name
    
class VideoItem(Item, Model):
    heading = models.TextField()
    content = RichTextField()
    videoLink = models.TextField()
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

    def __str__(self):
        return self.heading
    
class Portfolio(Component, Model):
    name = models.CharField(max_length=100)
    childModel = 'PortfolioItem'

    def __str__(self):
        return self.name
    
class PortfolioItem(Item, Model):
    heading = models.TextField()
    image = models.ImageField(upload_to='portfolio/%Y/%m/%d')
    link = models.TextField()
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)

    def __str__(self):
        return self.heading
    
class Services(Component, Model):
    name = models.CharField(max_length=100)
    childModel = 'ServicesItem'

    def __str__(self):
        return self.name
    
class ServicesItem(Item, Model):
    heading = models.TextField()
    content = RichTextField()
    link = models.TextField()
    icon = models.CharField(max_length=200)
    services = models.ForeignKey(Services, on_delete=models.CASCADE)

    def __str__(self):
        return self.heading
    
class Header(models.Model, Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='portfolio/%Y/%m/%d')
    image_alt = models.TextField()

    def __str__(self):
        return self.name
        
class Footer(models.Model, Model):
    name = models.CharField(max_length=100)
    facebook = models.CharField(max_length=100)
    google = models.CharField(max_length=100)
    twitter = models.CharField(max_length=100)
    vimeo = models.CharField(max_length=100)
    pinterest = models.CharField(max_length=100)
    about_us = RichTextField()
    open_hours = RichTextField()
    newsletter = RichTextField()

    def __str__(self):
        return self.name