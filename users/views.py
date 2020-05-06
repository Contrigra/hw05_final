from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')  # login is name attribute in path()
    template_name = 'signup.html'


def user_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            return redirect('/thank-you')

        return render(request, 'contact.html', {'form': form})
    form = ContactForm()
    return render(request, 'contact.html', {'form': form})

