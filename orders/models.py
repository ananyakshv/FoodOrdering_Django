from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Category Model to represent different food categories
from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True)  # Allow null and blank

    def save(self, *args, **kwargs):
        if not self.slug:  # Generate slug if not already set
            self.slug = slugify(self.name)
        
        # Check if slug already exists and modify if necessary
        if Category.objects.filter(slug=self.slug).exclude(id=self.id).exists():
            self.slug = f"{self.slug}-{self.pk}"  # Add primary key if slug exists

        super().save(*args, **kwargs)


    def __str__(self):
        return self.name


# FoodItem Model to represent individual food items
class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='food_images/', null=True, blank=True)  # Optional image field

    def __str__(self):
        return self.name

    def formatted_price(self):
        return f"₹{self.price:,.2f}"  # Optional: Add a method to format price nicely


# UserEngagement Model to store like/dislike actions from users on food items
class UserEngagement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.food_item.name} - {'Liked' if self.liked else 'Disliked'}"

from .models import FoodItem  # Assuming FoodItem model exists

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(FoodItem)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.TextField()
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

# orders/models.py
from django.db import models

class RecentlyLiked(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    food_item = models.ForeignKey('FoodItem', on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} liked {self.food_item.name}"
