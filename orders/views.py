from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.core.mail import send_mail
from .models import Category, FoodItem, UserEngagement
from .forms import ContactForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import FoodItem, RecentlyLiked

# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Authenticate user and log them in
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful.")
                return redirect('home')  # Redirect to home page or dashboard
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Please correct the errors above.")
    else:
        form = AuthenticationForm()

    return render(request, 'orders/login.html', {'form': form})


# Food Menu View (Handle likes/dislikes)
@login_required
def food_menu(request):
    categories = Category.objects.all()

    # Fetch recently liked items for the user
    recently_liked = RecentlyLiked.objects.filter(user=request.user).order_by('-liked_at')[:5]  # Latest 5 liked items

    if request.method == 'POST':
        for category in categories:
            for item in category.items.all():
                like_key = f"like_{item.id}"
                dislike_key = f"dislike_{item.id}"

                if like_key in request.POST:
                    UserEngagement.objects.update_or_create(
                        user=request.user,
                        food_item=item,
                        defaults={'liked': True}
                    )
                    messages.success(request, f"You liked {item.name}!")
                elif dislike_key in request.POST:
                    UserEngagement.objects.update_or_create(
                        user=request.user,
                        food_item=item,
                        defaults={'liked': False}
                    )
                    messages.success(request, f"You disliked {item.name}!")

        return redirect('food_menu')

    return render(request, 'orders/food_menu.html', {
        'categories': categories,
        'recently_liked': recently_liked
    })


# Contact Support View
def contact_support(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']
            
            # Send email to customer support
            send_mail(
                subject,
                message,
                email,
                [settings.SUPPORT_EMAIL],  # You need to define SUPPORT_EMAIL in settings
            )
            messages.success(request, "Your message has been sent successfully!")
            return redirect('food_menu')  # Redirect to food menu after successful submission
        else:
            messages.error(request, "Please fix the errors in the form.")
    else:
        form = ContactForm()

    return render(request, 'orders/contact_support.html', {'form': form})


# Home View
@login_required  # Ensure the user is logged in to access this page
def home_view(request):
    return render(request, 'orders/home.html')  # Template path


# Recent Likes View
@login_required
def recent_likes(request):
    if request.user.is_authenticated:
        # Fetch recent liked items (limit to 5 most recent liked items)
        recent_liked_items = UserEngagement.objects.filter(user=request.user, liked=True).order_by('-timestamp')[:5]
        return render(request, 'orders/recent_likes.html', {'recent_liked_items': recent_liked_items})
    else:
        # If the user is not logged in, redirect to login page
        return redirect('login')


# User Registration View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = UserCreationForm()

    return render(request, 'orders/register.html', {'form': form})


# A simple test view to check if templates are loaded correctly
def test_view(request):
    return render(request, 'orders/home.html')  # Make sure home.html exists

from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.http import JsonResponse
from .models import FoodItem, User

# View to handle the 'like' button click
from django.http import JsonResponse
from .models import FoodItem, RecentlyLiked
from django.shortcuts import get_object_or_404

# orders/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import FoodItem, RecentlyLiked

# views.py
from django.shortcuts import render, redirect
from .models import FoodItem, RecentlyLiked
from django.contrib.auth.decorators import login_required

from datetime import datetime
import logging

logger = logging.getLogger(__name__)

from django.shortcuts import redirect, get_object_or_404
from .models import FoodItem, RecentlyLiked
from django.contrib.auth.decorators import login_required

@login_required
def like_food(request, item_id):
    # Get the food item the user is trying to like
    food_item = get_object_or_404(FoodItem, id=item_id)
    
    # Create or update the RecentlyLiked object for the user
    RecentlyLiked.objects.update_or_create(
        user=request.user,
        food_item=food_item,
        defaults={'liked_at': timezone.now()}  # You can add other fields as needed
    )
    
    # Redirect back to the food menu page or where you want
    return redirect('food_menu')

@login_required
def dislike_food(request, item_id):
    # Get the food item the user is trying to dislike
    food_item = get_object_or_404(FoodItem, id=item_id)
    
    # You can handle the dislike logic here (e.g., remove from RecentlyLiked, etc.)
    RecentlyLiked.objects.filter(user=request.user, food_item=food_item).delete()
    
    # Redirect back to the food menu page or where you want
    return redirect('food_menu')

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import FoodItem, Order
import json

# Add to Cart Function
def add_to_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data['product_id']
        product_name = data['product_name']
        product_price = data['product_price']
        
        # Initialize cart if it doesn't exist in the session
        cart = request.session.get('cart', {})

        # Check if item already exists in the cart
        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] += 1  # Increase quantity
        else:
            # Add the item to the cart with quantity = 1
            cart[str(product_id)] = {
                'name': product_name,
                'price': product_price,
                'quantity': 1
            }

        # Save the updated cart back to session
        request.session['cart'] = cart

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})

# Update Cart Quantity


from django.http import JsonResponse
from .models import FoodItem

def update_cart(request, item_id):
    if request.method == 'POST':
        data = json.loads(request.body)  # Parse the JSON body
        quantity = data.get('quantity')

        # Ensure quantity is valid
        if quantity is not None and quantity > 0:
            cart = request.session.get('cart', {})
            if str(item_id) in cart:
                cart[str(item_id)]['quantity'] = quantity  # Update the quantity
                request.session['cart'] = cart
                return JsonResponse({'success': True, 'quantity': quantity})

        return JsonResponse({'success': False})
    return JsonResponse({'success': False})


# Remove Item from Cart
def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    if str(item_id) in cart:
        del cart[str(item_id)]  # Remove the item from the cart
        request.session['cart'] = cart
    return redirect('cart')

# Place Order Function
def place_order(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            return redirect('cart')  # Ensure cart is not empty
        
        total_price = sum(item['price'] * item['quantity'] for item in cart.values())  # Calculate total price
        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            address=request.POST['address'],  # Make sure address is passed correctly
            payment_method=request.POST['payment_method']
        )
        
        # Add items to the order (use the food_item object)
        for item in cart.values():
            food_item = FoodItem.objects.get(name=item['name'])
            # Add food item to the order, also including quantity
            order.items.add(food_item, through_defaults={'quantity': item['quantity']})
        
        # Clear cart after order is placed
        request.session['cart'] = {}
        
        return redirect('order_confirmation')  # Redirect to order confirmation page

    return render(request, 'order_confirmation.html')  # If not POST, render the order page

# views.py
from django.shortcuts import render

def order_confirmation(request):
    return render(request, 'orders/order_confirmation.html')
