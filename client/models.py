from django.db import models

class Slider(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SliderItem(models.Model):
    heading = models.TextField()
    description = models.TextField()
    left_button = models.CharField(max_length=200)
    right_button = models.CharField(max_length=200)
    background = models.ImageField(upload_to='slider/%Y/%m/%d')
    slider = models.ForeignKey(Slider, on_delete=models.CASCADE)

    def __str__(self):
        return self.heading
