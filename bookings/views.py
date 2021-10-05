from django.shortcuts import render
from .serializers import BookingSerializer
from rest_framework import viewsets, mixins, filters
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
    filterset_fields = ['car',]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        else:
            return Booking.objects.filter(user=user)
