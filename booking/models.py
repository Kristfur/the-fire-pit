from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

TIME_SLOTS = ((1, "2:00pm - 3:45pm"), (2, "4:00pm - 5:45pm"),
              (3, "6:00pm - 7:45pm"), (4, "8:00pm - 9:45pm"))


class AvailableBookings(models.Model):
    """
    Available bookings is how many tables the resturaunt has.
    It is used to check the capacity when a user creates a booking
    """
    available_tables_small = models.IntegerField(default=0)
    seats_per_table_small = models.IntegerField(default=0)
    available_tables_medium = models.IntegerField(default=0)
    seats_per_table_medium = models.IntegerField(default=0)
    available_tables_large = models.IntegerField(default=0)
    seats_per_table_large = models.IntegerField(default=0)
    updated_on = models.DateTimeField(default=0)
    updated_by = models.ForeignKey(
        User, default=0, on_delete=models.SET_DEFAULT,
        related_name="available_bookings"
    )

    def save(self, *args, **kwargs):
        self.updated_on = datetime.today()
        super().save(*args, **kwargs)


class Booking(models.Model):
    """
    Booking model for each reservation, has an owner who can edit it
    """
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="customer")
    booking_name = models.CharField(max_length=30)
    tables_needed_small = models.IntegerField(default=0)
    tables_needed_medium = models.IntegerField(default=0)
    tables_needed_large = models.IntegerField(default=0)
    guest_count = models.IntegerField(default=2)
    booking_date = models.DateField()
    booking_time = models.IntegerField(choices=TIME_SLOTS, default=1)

    class Meta:
        ordering = ['booking_date', 'booking_time']

    def __str__(self):
        return str(self.pk)
