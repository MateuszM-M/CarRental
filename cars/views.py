from django.shortcuts import render
from rest_framework import viewsets, mixins
from .models import Car, CarPhoto
from .serializers import CarSerializer, CarPhotoSerializer
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser, AllowAny
from .permissions import IsAdminUserOrReadOnly
     

class CarViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for staff
    and 'list' , 'retrieve' for any user.
    """
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    

class CarPhotoViewSet(viewsets.ModelViewSet):    
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for staff
    """
    queryset = CarPhoto.objects.all()
    serializer_class = CarPhotoSerializer
    permission_classes = [IsAdminUser]
    
    
