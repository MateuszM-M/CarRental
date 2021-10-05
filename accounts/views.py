from django.shortcuts import render
from .serializers import UserSerializer, LogoutSerializer
from rest_framework import viewsets, mixins, status, generics
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .permissions import IsNotAuthenticated
from rest_framework_simplejwt.tokens import (
    RefreshToken, OutstandingToken, BlacklistedToken
    )
from rest_framework.views import APIView


class CreateUserViewSet(mixins.CreateModelMixin,
                                viewsets.GenericViewSet):
    """
    A viewset for registering user instances.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsNotAuthenticated]
    
   
class ListRetrieveUserViewSet(mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    """
    A viewset for viewing user instances by staff.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]


class LogoutView(APIView):
    """
    View for logging out by blacklisting a currnetly used token.
    """
    
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    
class LogoutAllView(APIView):
    """
    View for logging out by blacklisting all outstanding tokens
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)