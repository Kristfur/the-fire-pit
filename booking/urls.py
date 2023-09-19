from django.urls import path
from booking.views import booking_home_page

urlpatterns = [
    path('bookings', booking_home_page.as_view(), name='booking_home')
    ]
