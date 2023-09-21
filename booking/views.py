from datetime import timedelta, date
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView, CreateView, UpdateView, ListView
from .models import AvailableBookings, Booking
from .forms import BookingForm


class booking_home_page(LoginRequiredMixin, ListView):
    """
    View to render my bookings page, user can 
    create, read, edit and delete their bookings from this page
    """
    model = Booking
    template_name = 'booking/booking_home.html'

    def get_bookings(self):
        return Booking.objects.filter(
            customer=self.request.user,
            booking_date__gt=(date.today()-timedelta(days=1))
            )
