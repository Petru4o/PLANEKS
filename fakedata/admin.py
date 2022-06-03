from django.contrib import admin

from .models import Schema, UserChoice, SlotChoice

# Register your models here.

admin.site.register(Schema)
admin.site.register(UserChoice)
admin.site.register(SlotChoice)
