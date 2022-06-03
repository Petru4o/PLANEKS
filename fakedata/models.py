from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Schema(models.Model):

    Separator_choices = [
        (',', 'Comma(,)'),
        (';', 'Semicolon(;)')
    ]

    Quotes_choices = [
        ('"', 'Double quotes (")'),
        ("'", "Single quotes (')"),
    ]

    schema_name = models.CharField(max_length=20)
    modified = models.DateField(auto_now_add=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    separator = models.CharField(max_length=20, choices=Separator_choices)
    quotes = models.CharField(max_length=20, choices=Quotes_choices)

    def __str__(self):
        return self.schema_name

class Column(models.Model):

    Column_type_choices = [
        ('Full name', 'full name'),
        ('Job', 'Jjb'),
        ('Email', 'email'),
        ('Domain name', 'domain name'),
        ('Phone number', 'phone number'),
        ('Company name', 'company name'),
        ('Text', 'text'),
        ('Integer', 'integer'),
        ('Address', 'address'),
        ('Date', 'date')
    ]

    column_name = models.CharField(max_length=20)
    column_type = models.CharField(max_length=20, choices=Column_type_choices)

    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)

    order = models.PositiveIntegerField(null=True)

    min_number = models.IntegerField(null=True, blank=True)
    max_number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.column_name} - {self.column_type}'


class FakeDataset(models.Model):
    Status = [
        ('Ready', 'ready'),
        ('Processing', 'processing')
    ]

    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Status)
    rows = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.schema.schema_name} - {self.status}'

