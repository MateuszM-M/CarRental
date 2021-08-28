from rest_framework import serializers
from django.contrib.auth.models import User
from django.core import exceptions
import django.contrib.auth.password_validation as validators


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        # style={'input_type': 'password'}
        )
    password2 = serializers.CharField(
        label='Confirm password', 
        write_only=True,
        # style={'input_type': 'password'},
        required=False
        )
    
    class Meta:
        model = User
        fields = ('id', 'username', "email", "password", "password2")
        extra_kwargs = {
            'password': {'write_only': True},
            'password2': {'write_only': True},
            }
        
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
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
                
