from django.contrib import admin

from .models import Schema, FakeDataset, Column

admin.site.register(Schema)
admin.site.register(FakeDataset)
admin.site.register(Column)

