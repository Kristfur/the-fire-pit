from django.db import models
from django.contrib.auth.models import User

TIME_SLOTS = ((1, "2:00pm - 3:45pm"), (2, "4:00pm - 5:45pm"),
              (3, "6:00pm - 7:45pm"), (4, "8:00pm - 9:45pm"))


class AvailableBookings(models.Model):
    available_tables = models.CharField(max_length=40)  # e.g (4, 2, 2) <- there are 4 tables with 4 seats, 2 with 6 and 2 with 8
    seats_per_table = models.CharField(max_length=40)   # e.g (4, 6, 8)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User, default=0, on_delete=models.SET_DEFAULT, related_name="available_bookings"
    )


class Booking(models.Model):
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="booking_customer")
    booking_name = models.CharField(max_length=25)
    tables_needed = models.CharField(max_length=40)
    guest_count = models.IntegerField(default=2)
    booking_date = models.DateField()
    booking_time = models.IntegerField(choices=TIME_SLOTS, default=1)

    class Meta:
        ordering = ['booking_date', 'booking_time']

    def __str__(self):
        return str(self.pk)
