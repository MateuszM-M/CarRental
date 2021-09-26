from rest_framework import serializers
from .models import Booking
from cars.serializers import CarSerializer

class BookingSerializer(serializers.ModelSerializer):
    car = CarSerializer(read_only=True)
    
    class Meta:
        model = Booking
        fields = ['user', 'car', 'booking_start', 'booking_end']