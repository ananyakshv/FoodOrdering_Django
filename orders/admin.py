

# Register your models here.
from django.contrib import admin
from .models import Category, FoodItem, UserEngagement

# Register your models here.
admin.site.register(Category)
admin.site.register(FoodItem)
admin.site.register(UserEngagement)
