from django.views.generic import TemplateView


class home_page(TemplateView):
    template_name = 'home/index.html'
