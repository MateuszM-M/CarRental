from django.shortcuts import render
from rest_framework import viewsets
from .models import Car

class CarViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`
    """
    queryset = Car.objects.all()
    serializer_class = CarSerializer