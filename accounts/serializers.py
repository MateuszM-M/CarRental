from rest_framework import serializers
from django.contrib.auth.models import User
from django.core import exceptions
import django.contrib.auth.password_validation as validators
from rest_framework.exceptions import ValidationError
from .models import Profile
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'city', 
                  'street', 'number', 'phone')
        

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        )
    password2 = serializers.CharField(
        label='Confirm password', 
        write_only=True,
        style={'input_type': 'password'}
        )
    
    class Meta:
        model = User
        fields = ('id', 'username', "email", "password", "password2", 'profile')
        
    def validate_password2(self, value):
        data = self.get_initial()
        password = data.get('password')
        password2 = value
        if password != password2:
            raise ValidationError('Passwords must match')
        return super(UserSerializer, self).validate(value)
        
    def validate_password(self, value):
        password = value
        errors = dict()
        try:
            validators.validate_password(password=password)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)
            if errors:
                raise serializers.ValidationError(errors)
        return super(UserSerializer, self).validate(value)
    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        Profile.objects.create(user=user, **profile_data)
        return user
                

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, value):
        self.token = value['refresh']
        return value

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')