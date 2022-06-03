from django.db import models
from django.contrib.auth.models import User


class Schema(models.Model):
    COMMA = ','
    SEMICOLON = ';'
    DOUBLEQUOTE = '"'
    SINGLEQUOTE = "'"

    Separator_choices = [
        (COMMA, 'Comma (,)'),
        (SEMICOLON, 'Semicolon (;)')
    ]
    Quotes_choices = [
        (DOUBLEQUOTE, 'Double-quote (")'),
        (SINGLEQUOTE, "Single-quote (')")
    ]

    schema_name = models.CharField(max_length=200)
    modified = models.DateField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    separator = models.CharField(max_length=2, choices=Separator_choices)
    quotes = models.CharField(max_length=2, choices=Quotes_choices)

    def __str__(self):
        return self.schema_name


class Column(models.Model):
    FULL_NAME = 'Full name'
    JOB = 'Job'
    EMAIL = 'Email'
    DOMAIN_NAME = 'Domain name'
    PHONE_NUMBER = 'Phone number'
    COMPANY_NAME = 'Company name'
    TEXT = 'Text'
    INTEGER = 'Integer'
    ADDRESS = 'Address'
    DATE = 'Date'

    Column_type_choices = [
        (FULL_NAME, 'Full name'),
        (JOB, 'Job'),
        (EMAIL, 'Email'),
        (DOMAIN_NAME, 'Domain name'),
        (PHONE_NUMBER, 'Phone number'),
        (COMPANY_NAME, 'Company name'),
        (TEXT, 'Text'),
        (INTEGER, 'Integer'),
        (ADDRESS, 'Address'),
        (DATE, 'Date')
    ]
    column_name = models.CharField(max_length=200)
    column_type = models.CharField(max_length=12, choices=Column_type_choices)

    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)

    order = models.PositiveIntegerField(null=True)

    min_number = models.IntegerField(null=True, blank=True)
    max_number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.column_name} - {self.column_type}'


class FakeDataset(models.Model):
    class Status(models.TextChoices):
        READY = 'Ready'
        PROCESSING = "Processing"

    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=Status.choices)
    rows = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.schema.schema_name} - {self.status}'


