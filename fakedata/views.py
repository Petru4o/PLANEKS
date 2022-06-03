from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import response

from django.views.generic import View

from . import forms
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView

from fakedata.models import Schema


class UserList(ListView):
    model = Schema
    context_object_name = 'schema'
    template_name = 'home.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserList, self).dispatch(request, *args, **kwargs)


class Login(LoginView):
    template_name = 'login.html'


def create_schema(request):
    if request.method == 'POST':
        schema_form = forms.CreateSchema(request.POST)
        slots_form = forms.CreateSlotChoices(request.POST)
        if schema_form.is_valid() and slots_form.is_valid():
            schema_form.save()
            slots_form.save()
            return HttpResponseRedirect('')
        else:
            context = {'schema_form': schema_form, 'slots_form': slots_form}
    else:
        context = {'schema_form': forms.CreateSchema(), 'slots_form': forms.CreateSlotChoices()}

    return render(request, 'add_schema.html', context)
