from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from fakedata.models import Schema, Column

column_formset = inlineformset_factory(
            Schema, Column, fields=('column_name', 'column_type', 'order', 'min_number', 'max_number'),
            labels={'column_name': 'Column name', 'column_type': 'Type',
                    'order': 'Order', 'min_number': 'From', 'max_number': 'To'},
            can_order=False, can_delete=True
        )


class LoginV(LoginView):
    template_name = 'login.html'


class MainList(ListView):
    model = Schema
    template_name = 'home.html'


class SchemaCreateView(CreateView):
    model = Schema
    fields = ['schema_name', 'separator', 'quotes']
    success_url = reverse_lazy('home')
    template_name = 'schema_form.html'
    context_object_name = 'schema_list'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["columns"] = column_formset(self.request.POST)
        else:
            data["columns"] = column_formset()
        return data

    def form_valid(self, form):
        form.instance.user = self.request.user
        context = self.get_context_data()
        columns = context["columns"]

        if columns.is_valid():
            self.object = form.save()
            columns.instance = self.object
            columns.save()
        else:
            form.add_error(None, columns.errors)
            return super().form_invalid(form)

        return super().form_valid(form)

