from django.contrib.auth.views import LoginView
from django.views.generic import ListView

from fakedata.models import Schema


class LoginView(LoginView):
    template_name = 'login.html'


class MainList(ListView):
    model = Schema
    template_name = 'home.html'
