from django.shortcuts import render
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import Booking
from .serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    User have CRUD operations on own objects.
    Staff have CRUD operation on all objects.
    """
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['car',]
    page_size = 1
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        else:
            return Booking.objects.filter(user=user)

