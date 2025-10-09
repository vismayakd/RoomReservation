from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class RoomCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    base_price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name
    
class Room(models.Model):
    room_number = models.CharField(max_length=10, unique=True)
    category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE, related_name='rooms')
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='room_images',null=True,blank=True) 

    def __str__(self):
        return f"Room {self.room_number} - {self.category.name}"
    
class SpecialRate(models.Model):
    room_category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE, related_name='special_rates')
    start_date = models.DateField()
    end_date = models.DateField()
    rate_multiplier = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)

    def __str__(self):
        return f"{self.room_category} [{self.start_date} - {self.end_date}]"

class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reservations')
    start_date = models.DateField()
    end_date = models.DateField()
    customer_name = models.CharField(max_length=200)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    status = models.BooleanField(default=False)

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError("End date must be after start date.")

    def __str__(self):
        return f"{self.customer_name} - {self.room} ({self.start_date} to {self.end_date})"