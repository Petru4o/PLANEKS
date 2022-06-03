from django.conf import settings
from faker import Faker
from faker.providers import BaseProvider

import csv

from PLANEKS_task.celery import app
from fakedata.models import Schema, Column, FakeDataset


@app.task
def generator(dataset_id):

    fake = Faker()

    dataset = FakeDataset.objects.filter(id=dataset_id).first()

    schema = Schema.objects.filter(id=dataset.schema_id).first()
    columns = Column.objects.filter(schema=schema.id).order_by("order").values()
    separator = schema.separator
    quote = schema.quotes

    row_number = dataset.rows
    header = []
    all_rows = []
    for column in columns:
        header.append(column["name"])

    for row in range(row_number):
        raw_row = []
        for column in columns:
            column_type = column["column_type"]
            if column_type == 'Full name':
                data = fake.name()
            elif column_type == 'Job':
                data = fake.job()
            elif column_type == 'Email':
                data = fake.email()
            elif column_type == 'Domain name':
                data = fake.domain_name()
            elif column_type == 'Phone number':
                data = fake.phone()
            elif column_type == 'Company name':
                data = fake.company()
            elif column_type == 'Text':
                data = fake.sentences(
                    nb=fake.random_int(
                        min=column["min_number"] or 1,
                        max=column["max_number"] or 5
                    )
                )
                data = " ".join(data)

            elif column_type == 'Integer':
                data = fake.random_int(
                    min=column["min_number"] or 0,
                    max=column["max_number"] or 9999
                )
            elif column_type == 'Address':
                data = fake.address()
            elif column_type == 'Date':
                data = fake.date()
            else:
                data = None
            raw_row.append(data)
        all_rows.append(raw_row)

    with open(f'{settings.MEDIA_ROOT}schema_{schema.id}dataset_{dataset_id}.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=separator, quotechar=quote, quoting=csv.QUOTE_ALL)
        writer.writerow(header)
        writer.writerows(all_rows)

        dataset.status = dataset.Status.READY
        dataset.save()
    for column in columns:
        header.append(column["name"])
