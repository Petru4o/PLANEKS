from django import forms

from .models import FakeDataset


class DataSetForm(forms.ModelForm):
    class Meta:
        model = FakeDataset
        fields = ['rows']