from django.db import models
from django.urls import reverse


class MenuItem(models.Model):
    title = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    url = models.CharField(max_length=100, blank=True)
    named_url = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.named_url:
            return reverse(self.named_url)
        elif self.url:
            return self.url
        else:
            return '#'


class Menu(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
