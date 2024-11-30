from django.contrib import admin
from django.urls import path, include
from orders import views
from django.contrib import admin
from django.urls import path
from django.conf import settings  # Make sure this import is correct
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('orders/', include('orders.urls')),  # Directs to the orders app URLs
    path('food-menu/', views.food_menu, name='food_menu'),
    path('', views.home_view, name='home'),  # Root URL
    path('contact-support/', views.contact_support, name='contact_support'),
    path('login/', views.login_view, name='login'),
    # Removed duplicate home URL and unnecessary food-ordering include.
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
