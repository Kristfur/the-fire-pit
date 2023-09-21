from datetime import timedelta, date
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView, CreateView, UpdateView, ListView
from .models import AvailableBookings, Booking
from .forms import BookingForm
from django.contrib import messages


class booking_home_page(LoginRequiredMixin, ListView):
    """
    View to render my bookings page, user can 
    create, read, edit and delete their bookings from this page
    """
    model = Booking
    template_name = 'booking/booking_home.html'

    def get_bookings(self):
        return Booking.objects.filter(
            customer == self.request.user,
            booking_date__gt=(date.today()-timedelta(days=1))
            )


class create_booking(LoginRequiredMixin, CreateView):
    """
    Allows user to create bookings
    """
    form_class = BookingForm
    template_name = 'booking/create_booking.html'
    success_url = "bookings"
    model = Booking

    def form_valid(self, form):
        """
        Assign booking to tables in an efficient manner
        """
        form.instance.customer = self.request.user
        date = form.cleaned_data['booking_date']
        time = form.cleaned_data['booking_time']
        guests = form.cleaned_data['guest_count']

        # Get all booking for this time
        bookings_at_same_time = Booking.objects.filter(
            booking_date=date, booking_time=time)

        available_tables = []
        seats_per_table = []

        # Get all available tables for this time
        for available in AvailableBookings.objects.all():
            available_tables = list(map(int, available.available_tables.split(",")))
            seats_per_table = list(map(int, available.seats_per_table.split(",")))

        # Remove occupied tables from available tables
        for booking in bookings_at_same_time:
            tables_used = list(map(int, booking.tables_needed.split(",")))
            for i in range(0, len(tables_used)):
                available_tables[i] -= tables_used[i]

        # Assign tables to booking,    ######(currently unoptomized)######
        unseated_guests = guests
        tables_needed = [0, 0, 0]
        while True:
            # Check large
            if available_tables[2] > 0:
                if unseated_guests >= seats_per_table[2]:
                    tables_needed[2] += 1
                    unseated_guests -= seats_per_table[2]
                    continue
            # Check medium
            if available_tables[1] > 0:
                if unseated_guests >= seats_per_table[1]:
                    tables_needed[1] += 1
                    unseated_guests -= seats_per_table[1]
                    continue
            # Check small
            if available_tables[0] > 0:
                if unseated_guests >= seats_per_table[0]:
                    tables_needed[0] += 1
                    unseated_guests -= seats_per_table[0]
                    break
            if available_tables[0] > 0:
                if unseated_guests < seats_per_table[0]:
                    tables_needed[0] += 1
                    unseated_guests -= seats_per_table[0]
                    break

        # Assign tables needed to booking
        form.instance.tables_needed = ','.join(map(str, tables_needed))

        messages.success(
            self.request,
            f'Booking confirmed for {guests} guests on {date}'
        )

        return super(create_booking, self).form_valid(form)


class edit_booking(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    User can edit their existing bookings through this view
    """

    form_class = BookingForm
    template_name = 'booking/edit_booking.html'
    success_url = "bookings"
    model = Booking

    def form_valid(self, form):
        """
        Assign booking to tables in an efficient manner
        """
        date = form.cleaned_data['booking_date']
        time = form.cleaned_data['booking_time']
        guests = form.cleaned_data['guest_count']

        # Get booking object
        tables_booked = Booking.objects.get(id=self.get_object().id)   # Add this code into form.py

        # Get all booking for this time
        bookings_at_same_time = Booking.objects.filter(
            booking_date=date, booking_time=time)

        available_tables = []
        seats_per_table = []

        # Get all available tables for this time
        for available in AvailableBookings.objects.all():
            available_tables = list(map(int, available.available_tables.split(",")))
            seats_per_table = list(map(int, available.seats_per_table.split(",")))

        # Remove occupied tables from available tables
        for booking in bookings_at_same_time:
            tables_used = list(map(int, booking.tables_needed.split(",")))
            for i in range(0, len(tables_used)):
                available_tables[i] -= tables_used[i]

        # Add currently booked table to available tables
        tables_used = list(map(int, tables_booked.tables_needed.split(",")))
        for i in range(0, len(tables_used)):
            available_tables[i] += tables_used[i]

        # Assign tables to booking,    ######(currently unoptomized)######
        unseated_guests = guests
        tables_needed = [0, 0, 0]
        while True:
            # Check large
            if available_tables[2] > 0:
                if unseated_guests >= seats_per_table[2]:
                    tables_needed[2] += 1
                    unseated_guests -= seats_per_table[2]
                    continue
            # Check medium
            if available_tables[1] > 0:
                if unseated_guests >= seats_per_table[1]:
                    tables_needed[1] += 1
                    unseated_guests -= seats_per_table[1]
                    continue
            # Check small
            if available_tables[0] > 0:
                if unseated_guests >= seats_per_table[0]:
                    tables_needed[0] += 1
                    unseated_guests -= seats_per_table[0]
                    break
            if available_tables[0] > 0:
                if unseated_guests < seats_per_table[0]:
                    tables_needed[0] += 1
                    unseated_guests -= seats_per_table[0]
                    break

        # Assign tables needed to booking
        form.instance.tables_needed = ','.join(map(str, tables_needed))

        messages.success(
            self.request,
            f'Successfully updated booking for {guests} guests on {date}'
        )
        return super(edit_booking, self).form_valid(form)

    def test_func(self):
        """ Test user is staff or throw 403 """
        if self.request.user.is_staff:
            return True
        else:
            return self.request.user == self.get_object().customer


class delete_booking(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Allows user to delete their bookings
    """
    model = Booking
    success_url = "bookings"

    def form_valid(self, form):
        """
        Display toast message on successf delete 
        """
        messages.success(
            self.request,
            'Successfully deleted booking'
        )
        return super(delete_booking, self).form_valid(form)

    def test_func(self):
        """ Test user is staff else throw 403 """
        if self.request.user.is_staff:
            return True
        else:
            return self.request.user == self.get_object().customer
