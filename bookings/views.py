from django.shortcuts import render
from .serializers import BookingSerializer
from rest_framework import viewsets, mixins
from .models import Booking
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class BookingViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    User have CRUD operations on own objects.
    Staff have Crud operation on all objects.
    """
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        else:
            return Booking.objects.filter(user=user)
    
    
class UserBookingViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing booking instances
    by authenticated user.
    """
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        This should return a list of all the bookings
        for the currently authenticated user.
        """
        user = self.request.user.id
        return Booking.objects.filter(user=user)
    
  