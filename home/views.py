from django.views.generic import TemplateView


class HomePage(TemplateView):
    """
    Render the home page
    """
    template_name = 'home/index.html'
