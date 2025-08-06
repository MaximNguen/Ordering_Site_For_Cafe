from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='menu/', blank=True, null=True, verbose_name='Картинка')
    description = models.TextField()
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Dish(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название блюда')
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='dishes',
        verbose_name='Категория'
    )
    description = models.TextField(verbose_name='Описание')
    price = models.IntegerField(max_length=10, verbose_name='Цена')
    image = models.ImageField(upload_to='dishes/', blank=True, null=True, verbose_name='Изображение')
    image2 = models.ImageField(upload_to='dishes/', blank=True, null=True, verbose_name='Изображение для описании')

    is_available = models.BooleanField(default=True, verbose_name='Доступно')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'