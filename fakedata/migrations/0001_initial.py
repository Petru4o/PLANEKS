# Generated by Django 4.0.5 on 2022-06-03 08:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Schema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schema_name', models.CharField(max_length=20)),
                ('modified', models.DateField(auto_now_add=True)),
                ('separator', models.CharField(choices=[(',', 'Comma(,)'), (';', 'Semicolon(;)')], max_length=20)),
                ('quotes', models.CharField(choices=[('"', 'Double quotes (")'), ("'", "Single quotes (')")], max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FakeDataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Ready', 'ready'), ('Processing', 'processing')], max_length=20)),
                ('rows', models.IntegerField(null=True)),
                ('schema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fakedata.schema')),
            ],
        ),
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column_name', models.CharField(max_length=20)),
                ('column_type', models.CharField(choices=[('Full name', 'full name'), ('Job', 'Jjb'), ('Email', 'email'), ('Domain name', 'domain name'), ('Phone number', 'phone number'), ('Company name', 'company name'), ('Text', 'text'), ('Integer', 'integer'), ('Address', 'address'), ('Date', 'date')], max_length=20)),
                ('order', models.PositiveIntegerField(null=True)),
                ('min_number', models.IntegerField(blank=True, null=True)),
                ('max_number', models.IntegerField(blank=True, null=True)),
                ('schema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fakedata.schema')),
            ],
        ),
    ]