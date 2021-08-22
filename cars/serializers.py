from rest_framework import serializers
from .models import Car

class CarSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'engine', 'year', 'location', 
                  'condition', 'day_price', 'hour_price']