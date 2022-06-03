from django import forms
from .models import Schema, SlotChoice, UserChoice


class CreateSchema(forms.ModelForm):
    class Meta:
        model = Schema
        fields = ('schema_name', 'column_separator', 'string_character', )


class CreateSlotChoices(forms.ModelForm):
    class Meta:
        model = SlotChoice
        fields = ('data_type', 'column_name', 'order', )

