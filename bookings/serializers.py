from rest_framework import serializers
from .models import Booking
from cars.serializers import CarSerializer

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, 
        default=serializers.CurrentUserDefault())
    car = CarSerializer()
    
    class Meta:
        model = Booking
        fields = ['user', 'car', 'booking_start', 'booking_end']
            
    def save(self, **kwargs):
        """Include default for read_only `user` field"""
        kwargs["user"] = self.fields["user"].get_default()
        return super().save(**kwargs)