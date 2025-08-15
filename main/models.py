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
    time_type = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='menu/', blank=True, null=True, verbose_name='Картинка')
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)

class Vacancy(models.Model):
    name = models.CharField(max_length=100)
    time_type = models.CharField(max_length=100)
    salary = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)