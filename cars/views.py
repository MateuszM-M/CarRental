from django.shortcuts import render
from rest_framework import viewsets, mixins
from .models import Car, CarPhoto
from .serializers import CarSerializer, CarPhotoSerializer
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser
     

class CarViewSet(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):
    """
    This viewset automatically provides `list`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    

class CreateCarViewSet(mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    """
    View for creating cars by staff
    """
    serializer_class = CarSerializer
    permission_classes = [IsAdminUser]
    

class AddCarPhotoViewSet(mixins.CreateModelMixin,
                  viewsets.GenericViewSet):    
    """
    View for adding car photos by staff
    """
    serializer_class = CarPhotoSerializer
    permission_classes = [IsAdminUser]
    
    
