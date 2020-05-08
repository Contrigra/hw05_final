from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm


class SignUpView(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')  # login is name attribute in path()
    template_name = 'signup.html'
