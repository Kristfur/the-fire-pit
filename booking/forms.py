from datetime import datetime
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django import forms
from .models import Booking, AvailableBookings


class BookingForm(forms.ModelForm):
    """
    Form to create and edit bookings
    """
    class Meta:
        model = Booking
        fields = [
            'booking_name', 'guest_count', 'booking_date', 'booking_time'
            ]
        booking_date = forms.DateField(help_text="Choose a date in the future")
        labels = {
            'booking_name': 'Name',
            'guest_count': 'Number Of Guests',
            'booking_date': 'Date',
            'booking_time': 'Time',
        }

    def clean(self):
        """
        Validate form data and throw errors when needed
        """
        date = self.cleaned_data['booking_date']
        time = self.cleaned_data['booking_time']
        guests = self.cleaned_data['guest_count']

        table_booked = None

        # Get booking object if it exists(to update it), or else pass
        try:
            table_booked = Booking.objects.get(id=self.instance.booked_table.id)
        except ObjectDoesNotExist:
            pass

        # Get all booking for this time
        bookings_at_same_time = Booking.objects.filter(
            booking_date=date, booking_time=time)

        available_tables = []
        seats_per_table = []

        # Get all available tables for this time
        for available in Available.objects.all():
            available_tables = list(map(int, available.available_tables.split(",")))
            seats_per_table = list(map(int, available.seats_per_table.split(",")))

        # Remove occupied tables from available tables
        for booking in bookings_at_same_time:
            tables_used = list(map(int, booking.tables_needed.split(",")))
            for i in range(0, len(tables_used)):
                available_tables[i] -= tables_used[i]

        # Add currently booked table to available tables
        if table_booked is not None:
            tables_used = list(map(int, table_booked.tables_needed.split(",")))
            for i in range(0, len(tables_used)):
                available_tables[i] -= tables_used[i]

        # Throw errors on form
        if date < datetime.today().date():
            raise ValidationError(
                'Invalid date - Booking cannot be in the past')
        if total_seats(available_tables, seats_per_table) < guests:
            raise ValidationError(
                'Sorry, there are no tables available to accomadate'
                + ' that amount of guests at this time.'
            )
        if sum(available_tables) == 0:
            raise ValidationError('Sorry, there are no tables available for this date and time')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['booking_date'].widget.attrs['class'] = 'datepicker'
        self.fields['booking_date'].widget.attrs['autocomplete'] = 'off'


def total_seats(tables, seats):
    """
    Counts all remaining available seats
    """
    count = 0
    for i in range(0, len(tables)):
        count += tables[i] * seats[i]
    return count
