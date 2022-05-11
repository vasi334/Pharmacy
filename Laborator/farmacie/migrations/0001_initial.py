# Generated by Django 3.2.9 on 2021-11-17 14:13

import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card_client',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True)),
                ('nume', models.CharField(max_length=200)),
                ('prenume', models.CharField(max_length=200)),
                (
                    'CNP',
                    models.CharField(
                        max_length=13,
                        unique=True,
                        validators=[django.core.validators.MinLengthValidator(
                            13)])
                ),
                ('data_nasterii', models.DateField()),
                ('data_inregistrarii', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Medicament',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True)),
                ('nume', models.CharField(max_length=200)),
                ('producator', models.CharField(max_length=200)),
                (
                    'pret',
                    models.FloatField(
                        validators=[django.core.validators.MinValueValidator(
                            0.0)])),
                ('necesita_reteta', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Tranzactie',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True)),
                (
                    'id_card_client',
                    models.CharField(blank=True, max_length=200, null=True)),
                (
                    'nr_bucati',
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(
                            0)]
                        )),
                ('data', models.DateField()),
                ('ora', models.TimeField()),
            ],
        ),
    ]
