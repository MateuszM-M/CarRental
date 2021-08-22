from django.shortcuts import render
from rest_framework import viewsets
from .models import Car, CarPhoto
from .serializers import CarSerializer, CarPhotoSerializer
from rest_framework.decorators import api_view


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'cars': reverse('car-list', request=request, format=format),
        'car-photos': reverse('car-photos', request=request, format=format),
    })
    
    

class CarViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    
    
