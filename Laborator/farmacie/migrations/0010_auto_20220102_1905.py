# Generated by Django 3.2.9 on 2022-01-02 17:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmacie',
            '0009_historicalcard_client_historicalmedicament_historicaltranzactie'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalmedicament',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicaltranzactie',
            name='history_user',
        ),
        migrations.DeleteModel(
            name='HistoricalCard_client',
        ),
        migrations.DeleteModel(
            name='HistoricalMedicament',
        ),
        migrations.DeleteModel(
            name='HistoricalTranzactie',
        ),
    ]