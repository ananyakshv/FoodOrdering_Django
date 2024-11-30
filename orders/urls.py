from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from . import views
# urls.py

from django.conf import settings  # Ensure this import is present
from django.conf.urls.static import static
from django.urls import path




urlpatterns = [
    path('food-menu/', views.food_menu, name='food_menu'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('home/', views.home_view, name='home'),
    path('contact_support/', views.contact_support, name='contact_support'),
    path('recent-likes/', views.recent_likes, name='recent_likes'),
    #path('test-register/', views.test_register_view),
    #path('test/', views.test_view),  # Test page
    path('signup/', views.register, name='signup'),  # Add this line for signup
    path('add-to-cart/<int:food_item_id>/', views.add_to_cart, name='add_to_cart'),
    path('like-food/<int:item_id>/', views.like_food, name='like_food'),
    path('dislike-food/<int:item_id>/', views.dislike_food, name='dislike_food'),
    # Other URLs...
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('update_cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # Place order and order confirmation
    path('place_order/', views.place_order, name='place_order'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)