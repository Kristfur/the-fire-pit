from django.urls import path
from . import views

urlpatterns = [
    path('bookings',
         views.BookingHomePage.as_view(),
         name='booking_home'),
    path('edit_booking/<slug:pk>',
         views.EditBooking.as_view(),
         name='edit_booking'),
    path('create_booking',
         views.CreateBooking.as_view(),
         name='create_booking'),
    path('delete_booking/<slug:pk>',
         views.DeleteBooking.as_view(),
         name='delete_booking'),
    path('my_account',
         views.MyAccount.as_view(),
         name='my_account'),
    path('setup_page/<slug:pk>',
         views.SetupPage.as_view(),
         name='setup_page'),
    ]
