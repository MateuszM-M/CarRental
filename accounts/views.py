from django.shortcuts import render
from .serializers import (
    UserSerializer, LogoutSerializer, EmailVerificationSerializer,
    ChangePasswordSerializer,
    )
from rest_framework import viewsets, mixins, status, generics, views
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from .permissions import IsNotAuthenticated
from rest_framework_simplejwt.tokens import (
    RefreshToken, OutstandingToken, BlacklistedToken
    )
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.decorators import action
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


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
        
    def create(self, request, *args, **kwargs):
        """
        Override of create method to send activation email
        """
        user = request.data
        serializer = self.get_serializer(data=user)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user_data = serializer.data
        user = User.objects.get(username=user_data['username'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')
        absurl = 'http://'+current_site+relative_link+"?token="+str(token)
        email_body = 'Hi '+user.username + \
            ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}
        
        Util.send_email(data)
        return Response(serializer.data, 
                        status=status.HTTP_201_CREATED, 
                        headers=headers)
                
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
        

class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer
        
        
class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    
    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY,
        description='Description',
        type=openapi.TYPE_STRING)
    
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, 
                                settings.SECRET_KEY, 
                                algorithms='HS256')
            user = User.objects.get(id=payload['user_id'])
            if not user.is_active:
                user.is_active = True
                user.save()
            return Response({'account': 'Successfully activated'}, 
                            status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        

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