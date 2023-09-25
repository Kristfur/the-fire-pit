from datetime import datetime
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django import forms
from .models import Booking, AvailableBookings


class BookingForm(forms.ModelForm):
    """
    Form to create and edit bookings
    """
    booking_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}),
                                   required=True)

    class Meta:
        model = Booking
        fields = [
            'booking_name', 'guest_count', 'booking_date', 'booking_time',
            ]

        labels = {
            'booking_name': 'Booking Name',
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

        tables_booked = [0, 0, 0]
        current_booking = ''

        # Get booking object if it exists(to update it), or else pass

        try:
            current_booking = Booking.objects.get(id=self.instance.id)
            tables_booked[0] = current_booking.tables_needed_small
            tables_booked[1] = current_booking.tables_needed_medium
            tables_booked[2] = current_booking.tables_needed_large
        except ObjectDoesNotExist:
            pass

        # Get all booking for this time
        bookings_at_same_time = Booking.objects.filter(
            booking_date=date, booking_time=time)

        available_tables = []
        seats_per_table = []
        tables_used = []

        # Get all available tables for this time
        for available in AvailableBookings.objects.all():
            available_tables.append(available.available_tables_small)
            seats_per_table.append(available.seats_per_table_small)
            available_tables.append(available.available_tables_medium)
            seats_per_table.append(available.seats_per_table_medium)
            available_tables.append(available.available_tables_large)
            seats_per_table.append(available.seats_per_table_large)

        # Remove occupied tables from available tables
        for booking in bookings_at_same_time:
            available_tables[0] -= booking.tables_needed_small
            available_tables[1] -= booking.tables_needed_medium
            available_tables[2] -= booking.tables_needed_large

        # Add currently booked table to available tables
        for i in range(0, 3):
            available_tables[i] += tables_booked[i]

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
        if guests <= 0:
            raise ValidationError('Sorry, you must book a table for at least one person')

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
