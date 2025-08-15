from django.contrib import admin
from main.models import Category, Promotions, Vacancy

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Promotions)
class PromotionsAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('name', 'time_type', 'salary', 'id')
    list_filter = ('time_type',)
    search_fields = ('name', 'description')
    ordering = ('id',)
