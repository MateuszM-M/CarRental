from django.shortcuts import render
from .serializers import BookingSerializer
from rest_framework import viewsets, mixins
from .models import Booking
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class BookingViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing booking instances
    by staff.
    """
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()
    permission_classes = [IsAdminUser]
    
    
class UserBookingViewSet(mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    """
    A viewset for viewing and editing booking instances
    by authenticated user.
    """
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        This view should return a list of all the bookings
        for the currently authenticated user.
        """
        user = self.request.user.id
        return Booking.objects.filter(user=user)
    

class CreateBookingViewSet(mixins.CreateModelMixin,
                                viewsets.GenericViewSet):
    """
    View for creating bookings by authenticated user.
    """
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    