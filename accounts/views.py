from django.shortcuts import render
from .serializers import UserSerializer
from rest_framework import viewsets, mixins, status
from django.contrib.auth.models import User
from rest_framework.response import Response


class CreateUserViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
   
    

        