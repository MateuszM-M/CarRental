"""CarRental URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts import views as accounts_views
from cars import views as cars_views
from bookings import views as bookings_views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register(r'cars', cars_views.CarViewSet)
router.register(r'add-car', 
                cars_views.CreateCarViewSet,
                basename='add-car')
router.register(r'add-car-photo', 
                cars_views.AddCarPhotoViewSet,
                basename='add-car-photo')
router.register(r'register', 
                accounts_views.CreateUserViewSet, 
                basename='register')
router.register(r'users', 
                accounts_views.ListRetrieveUserViewSet, 
                basename='users')
router.register(r'bookings', bookings_views.BookingViewSet)
router.register(r'my-bookings', 
                bookings_views.UserBookingViewSet, 
                basename='my-bookings')
router.register(r'create-booking', 
                bookings_views.CreateBookingViewSet, 
                basename='create-bookings')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', accounts_views.LogoutView.as_view(), name='logout'),
    path('logout-all/', accounts_views.LogoutAllView.as_view(), name='logout-all')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)