from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.forms import inlineformset_factory

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView
from django.views.generic.edit import FormMixin

from fakedata.models import Schema, Column, FakeDataset
from .tasks import generate_data_task
from .forms import DataSetForm

column_formset = inlineformset_factory(
    Schema, Column, fields=('column_name', 'column_type', 'order', 'min_number', 'max_number'),
    labels={'column_name': 'Column name', 'column_type': 'Type',
            'order': 'Order', 'min_number': 'From', 'max_number': 'To'},
    can_order=False, can_delete=True
)


class LoginV(LoginView):
    template_name = 'login.html'


class MainList(LoginRequiredMixin, ListView):
    model = Schema
    template_name = 'home.html'


class SchemaCreateView(LoginRequiredMixin, CreateView):
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


class DeleteSchemaView(LoginRequiredMixin, DeleteView):
    model = Schema
    success_url = reverse_lazy('home')
    template_name = 'schema_delete.html'


class DataSetView(LoginRequiredMixin, FormMixin, ListView):
    model = FakeDataset
    form_class = DataSetForm
    template_name = 'fakedataset_list.html'
    context_object_name = 'schema_datasets'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(schema_id=self.schema_id)

    def form_valid(self, form):
        form.instance.schema_id = self.schema_id
        form.instance.status = FakeDataset.Status.PROCESSING

        dataset = form.save()

        generate_data_task.delay(dataset.id)

        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        self.schema_id = kwargs["pk"]
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.path
