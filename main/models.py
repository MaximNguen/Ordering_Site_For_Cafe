from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='menu/', blank=True, null=True, verbose_name='Картинка')
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)

class Promotions(models.Model):
    name = models.CharField(max_length=100)
    redText = models.TextField()
    image = models.ImageField(upload_to='menu/', blank=True, null=True, verbose_name='Картинка')
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)
