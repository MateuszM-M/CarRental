from django.shortcuts import render
from .serializers import UserSerializer, LogoutSerializer
from rest_framework import viewsets, mixins, status, generics
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from .permissions import IsNotAuthenticated
from rest_framework_simplejwt.tokens import (
    RefreshToken, OutstandingToken, BlacklistedToken
    )
from rest_framework.views import APIView
from django.contrib.auth.models import User

class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    serializer_class = UserSerializer
    
    def get_permissions(self):
        """
        This method ensures that only unauthenticated user can regiser
        a new account. Action 'list' also retained in this permission
        so register form is still available in browseable api, get_queryset
        method ensures that no user detail could be listed.
        """
        if self.action in ('create',):
            permission_classes = [IsNotAuthenticated]
        elif self.action in ('list',):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        else:
            return User.objects.filter(username=user)
        
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


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