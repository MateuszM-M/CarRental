from django.db import models
from PIL import Image

class Car(models.Model):
    CONDITION = (
        ('used', 'used'),
        ('new', 'new'),
    )
    
    brand = models.CharField(max_length=40)
    model = models.CharField(max_length=50)
    engine = models.CharField(max_length=50)
    year = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    condition = models.CharField(max_length=50, choices=CONDITION)
    day_price = models.DecimalField(max_digits=6, decimal_places=2)
    hour_price = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return '{} {}'.format(self.brand, self.model)
    
    
class CarPhoto(models.Model):
    car = models.ForeignKey(Car, 
                            related_name='photos', 
                            on_delete=models.CASCADE)
    photo = models.ImageField(blank=True, null=True, upload_to='photos')
    
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)
        
        if img.height > 800 or img.width > 800:
            output_size = (800, 800)
            img.thumbnail(output_size)
            img.save(self.photo.path)