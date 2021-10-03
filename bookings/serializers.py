from rest_framework import serializers
from .models import Booking
from cars.serializers import CarSerializer
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from datetime import datetime, date


class BookingSerializer(serializers.ModelSerializer):
    car = CarSerializer()
    
    class Meta:
        model = Booking
        fields = ['user', 'car', 'booking_start', 'booking_end']
            
    
class CreateBookingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, 
        default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Booking
        fields = ['user', 'car', 'booking_start', 'booking_end']
        
    def validate(self, data):
        booking_start = data.get('booking_start')
        booking_end = data.get('booking_end')
        car = data.get('car')
        
        # car booked before start and ends after start
        case_1 = Booking.objects.filter(car=car,
                                        booking_start__lte=booking_start,
                                        booking_end__gte=booking_start
        ).exists()
        # car booked before booking end, booking end after request booking end
        case_2 = Booking.objects.filter(car=car,
                                        booking_start__lte=booking_end,
                                        booking_end__gte=booking_end
        ).exists()
        # booking "inside" requesteg booking
        case_3 = Booking.objects.filter(car=car,
                                        booking_start__gte=booking_start,
                                        booking_end__lte=booking_end
        ).exists()
        
        if case_1 or case_2 or case_3:
            raise ValidationError(
                'These dates are occupied'
                )
        return data
        
    def validate_booking_start(self, value):
        booking_start = value
        today_value = timezone.now().today().date()
        if booking_start < today_value:
            raise ValidationError(
                f'Booking start date must be greater than {today_value}'
                )
        return super(CreateBookingSerializer, self).validate(value)
    
    def validate_booking_end(self, value):
        data = self.get_initial()
        booking_start = data.get('booking_start')
        booking_start = datetime.strptime(booking_start, '%Y-%m-%d').date()
        booking_end = value
        if booking_end < booking_start:
            raise ValidationError(
                'Booking end date must be greater than booking start date'
                )
        return super(CreateBookingSerializer, self).validate(value)
            
    def save(self, **kwargs):
        """Include default for read_only `user` field"""
        kwargs["user"] = self.fields["user"].get_default()
        return super().save(**kwargs)