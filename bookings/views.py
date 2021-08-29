from django.shortcuts import render
from .serializers import BookingSerializer
from rest_framework import viewsets
from .models import Booking
from rest_framework.permissions import IsAdminUser


class BookingViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing booking instances.
    """
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()
    permission_classes = [IsAdminUser]
