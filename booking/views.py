from django.views.generic import TemplateView


class booking_home_page(TemplateView):
    template_name = 'booking/booking_home.html'
