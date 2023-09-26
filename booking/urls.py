from django.urls import path
from . import views

urlpatterns = [
    path('bookings',
         views.booking_home_page.as_view(),
         name='booking_home'),
    path('edit_booking/<slug:pk>',
         views.edit_booking.as_view(),
         name='edit_booking'),
    path('create_booking',
         views.create_booking.as_view(),
         name='create_booking'),
    path('delete_booking/<slug:pk>',
         views.delete_booking.as_view(),
         name='delete_booking'),
    path('my_account',
         views.my_account.as_view(),
         name='my_account'),
    ]
