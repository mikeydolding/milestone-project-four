from django.contrib import admin
from .models import Item, Category
# Register your models here.


class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
    )

    ordering = ('sku',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )

admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)