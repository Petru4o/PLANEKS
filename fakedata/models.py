from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class SlotChoice(models.Model):
    option_data_types = [
        ('Full name', 'full name'),
        ('Job', 'job'),
        ('Email', 'email'),
        ('Domain name', 'domain name'),
        ('Phone number', 'phone number'),
    ]

    data_type = models.CharField(max_length=20, choices=option_data_types)
    column_name = models.CharField(max_length=20)
    order = models.IntegerField(unique=True)
    schema_name = models.ForeignKey('Schema', max_length=20, related_name='reviews', on_delete=models.CASCADE)

    def __str__(self):
        return self.data_type + " " + self.column_name


class Schema(models.Model):
    option_separator = [
        ('Comma (,)', 'comma (,)'),
        ('Semicolon (;)', 'semicolon (;)')
    ]

    option_string_character = [
        ('Quote', 'quote'),
        ('Double-quote', 'double-quote')
    ]

    schema_name = models.CharField(max_length=20)
    column_separator = models.CharField(choices=option_separator, max_length=25)
    string_character = models.CharField(choices=option_string_character, max_length=25)

    def __str__(self):
        return self.schema_name

    # full_name = models.CharField(max_length=20)
    # job = models.CharField(max_length=20)
    # email = models.EmailField()
    # domain_name = models.CharField(max_length=20)
    # phone_number = models.CharField(max_length=13)
    # company_name = models.CharField(max_length=30)
    # text = models.TextField()
    # integer_field = models.IntegerField()
    # address = models.CharField(max_length=100)
    # date = models.DateField()


class UserChoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Schema, on_delete=models.CASCADE)

    def __str__(self):
        return self.user

