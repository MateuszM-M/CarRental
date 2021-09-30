from rest_framework import serializers
from .models import Car, CarPhoto


class CarPhotoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CarPhoto
        fields = ['car', 'photo']
        extra_kwargs = {
            'car': {'write_only': True},
        }


class CarSerializer(serializers.HyperlinkedModelSerializer):
    photos = CarPhotoSerializer(many=True, read_only=True)
        
    class Meta:
        model = Car
        fields = ['url', 'brand', 'model', 'engine', 'year', 'location', 
                  'condition', 'day_price', 'hour_price', 'photos']
        
