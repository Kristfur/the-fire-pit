from datetime import timedelta, date
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView, CreateView, UpdateView, ListView
from .models import AvailableBookings, Booking
from .forms import BookingForm, SetupForm
from django.contrib import messages


class booking_home_page(LoginRequiredMixin, ListView):
    """
    View to render my bookings page, user can
    create, read, edit and delete their bookings from this page
    """
    model = Booking
    template_name = 'booking/booking_home.html'

    def get_queryset(self):
        if self.request.user.is_staff:
            search_booking_ref = self.request.GET.get('booking_reference')
            search_dates = self.request.GET.get('date')
            if search_booking_ref:
                return Booking.objects.filter(id=search_booking_ref)
            if search_dates:
                return Booking.objects.filter(booking_date=search_dates)

            return Booking.objects.filter(
                booking_date__gt=(date.today()-timedelta(days=1))
                )
        else:
            return Booking.objects.filter(
                customer=self.request.user,
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
        form.instance.tables_needed_small = tables_needed[0]
        form.instance.tables_needed_medium = tables_needed[1]
        form.instance.tables_needed_large = tables_needed[2]

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
    success_url = "/"
    model = Booking

    def form_valid(self, form):
        """
        Assign booking to tables in an efficient manner
        """
        date = form.cleaned_data['booking_date']
        time = form.cleaned_data['booking_time']
        guests = form.cleaned_data['guest_count']

        # Get booking object
        tables_booked = [0, 0, 0]
        current_booking = Booking.objects.get(id=self.get_object().id)
        tables_booked[0] = current_booking.tables_needed_small
        tables_booked[1] = current_booking.tables_needed_medium
        tables_booked[2] = current_booking.tables_needed_large

        # Get all booking for this time
        bookings_at_same_time = Booking.objects.filter(
            booking_date=date, booking_time=time)

        available_tables = []
        seats_per_table = []

        # Get all available tables for this time
        available = AvailableBookings.objects.all()[0]
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

        # Assign tables to booking,    ######(currently unoptomized)######
        unseated_guests = guests
        tables_needed = [0, 0, 0]
        while True:
            # Check if everyone is seated
            if unseated_guests <= 0:
                break
            # Check large
            if available_tables[2] > 0:
                if unseated_guests > seats_per_table[1]:
                    tables_needed[2] += 1
                    available_tables[2] -= 1
                    unseated_guests -= seats_per_table[2]
                    continue
            # Check medium
            if available_tables[1] > 0:
                if unseated_guests > seats_per_table[0]:
                    tables_needed[1] += 1
                    available_tables[1] -= 1
                    unseated_guests -= seats_per_table[1]
                    continue
            # Check small
            if available_tables[0] > 0:
                tables_needed[0] += 1
                available_tables[0] -= 1
                unseated_guests -= seats_per_table[0]
                continue
            if available_tables[0] > 0:
                if unseated_guests < seats_per_table[0]:
                    tables_needed[0] += 1
                    unseated_guests -= seats_per_table[0]
                    break

        # Assign tables needed to booking
        form.instance.tables_needed_small = tables_needed[0]
        form.instance.tables_needed_medium = tables_needed[1]
        form.instance.tables_needed_large = tables_needed[2]
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
    success_url = "/"
    template_name = 'booking/confirm_delete.html'

    def form_valid(self, form):
        """
        Display toast message on success delete
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


class my_account(LoginRequiredMixin, ListView):
    """
    View to render my bookings page, user can
    create, read, edit and delete their bookings from this page
    """
    model = Booking
    template_name = 'booking/my_account.html'


class setup_page(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allows user to create bookings
    """
    form_class = SetupForm
    template_name = 'booking/setup_page.html'
    success_url = "/"
    model = AvailableBookings

    def form_valid(self, form):

        form.instance.updated_by = self.request.user

        messages.success(
            self.request,
            'Table setup has been changed successfully'
        )

        return super(setup_page, self).form_valid(form)

    def test_func(self):
        """ Test user is staff"""
        if self.request.user.is_staff:
            return True
        return False
