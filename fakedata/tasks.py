import csv

from django.conf import settings
from faker import Faker
from PLANEKS.celery import app


@app.task
def generate_data_task(dataset_id):
    from .models import Schema, Column, FakeDataset
    fake = Faker()

    dataset = FakeDataset.objects.filter(id=dataset_id).first()
    if not dataset:
        return
    schema = Schema.objects.filter(id=dataset.schema_id).first()
    columns = Column.objects.filter(schema=schema.id).order_by("order").values()
    delimeter = schema.separator
    quotechar = schema.quotes

    row_number = dataset.rows
    header = []
    all_rows = []
    for column in columns:
        header.append(column["column_name"])

    for row in range(row_number):
        raw_row = []
        for column in columns:
            column_type = column["column_type"]
            if column_type == Column.FULL_NAME:
                data = fake.name()
            elif column_type == Column.JOB:
                data = fake.job()
            elif column_type == Column.EMAIL:
                data = fake.email()
            elif column_type == Column.DOMAIN_NAME:
                data = fake.domain_name()
            elif column_type == Column.PHONE_NUMBER:
                data = fake.phone()
            elif column_type == Column.COMPANY_NAME:
                data = fake.company()
            elif column_type == Column.TEXT:
                data = fake.sentences(
                    nb=fake.random_int(
                        min=column["min_number"] or 1,
                        max=column["max_number"] or 10
                    )
                )
                data =" ".join(data)

            elif column_type == Column.INTEGER:
                data = fake.random_int(
                    min=column["min_number"] or 0,
                    max=column["max_number"] or 99999
                )
            elif column_type == Column.ADDRESS:
                data = fake.address()
            elif column_type == Column.DATE:
                data = fake.date()
            else:
                data = None
            raw_row.append(data)
        all_rows.append(raw_row)

    with open(f'{settings.MEDIA_ROOT}schema_{schema.id}dataset_{dataset_id}.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=delimeter, quotechar=quotechar, quoting=csv.QUOTE_ALL)
        writer.writerow(header)
        writer.writerows(all_rows)

        dataset.status = dataset.Status.READY
        dataset.save()