from rest_framework import serializers
from django.contrib.auth.models import User
from django.core import exceptions
import django.contrib.auth.password_validation as validators
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
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
        fields = ('id', 'username', "email", "password", "password2")
        
    def validate_password2(self, value):
        data = self.get_initial()
        password = data.get('password')
        password2 = value
        if password != password2:
            raise ValidationError('Passwords must match')
        breakpoint()
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
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
                
