from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Название точки (необязательно)')
    address = models.CharField(max_length=255, verbose_name='Адрес заведения')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    class Meta:
        verbose_name = 'Адрес заведения'
        verbose_name_plural = 'Адреса заведений'
        ordering = ['id']

    def __str__(self):
        return self.name or self.address
