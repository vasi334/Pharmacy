from django.shortcuts import render
from django.db import models
from django.core.validators import MinValueValidator, MinLengthValidator
import uuid


class Medicament(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False
        )
    nume = models.CharField(max_length=200)
    producator = models.CharField(max_length=200)
    pret = models.FloatField(validators=[MinValueValidator(0.0)])
    necesita_reteta = models.BooleanField()
    nr_vanzari = models.IntegerField(default=0)

    def project(request, pk):
        medicamentObj = Medicament.objects.get(id=pk)
        return render(
            request,
            'farmacie/single-project.html',
            {'medicamentObj': medicamentObj}
            )

    def __str__(self):
        return self.nume


class Card_client(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False)
    nume = models.CharField(max_length=200)
    prenume = models.CharField(max_length=200)
    CNP = models.CharField(
        max_length=13,
        validators=[MinLengthValidator(13)],
        unique=True)
    data_nasterii = models.DateField()
    data_inregistrarii = models.DateField()

    def carduri(request, pk):
        cardObj = Card_client.objects.get(id=pk)
        return render(
            request,
            'farmacie/single-card.html',
            {'cardObj': cardObj}
            )

    def __str__(self):
        return self.nume + ' ' + self.prenume


class Tranzactie(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False)
    id_card_client = models.CharField(max_length=200, null=True, blank=True)
    medicament = models.CharField(max_length=200)
    nr_bucati = models.IntegerField(validators=[MinValueValidator(0)])
    data = models.DateField()
    ora = models.TimeField()

    def tranzactii(request, pk):
        tranzactieObj = Tranzactie.objects.get(id=pk)
        return render(
            request,
            'farmacie/single-tranzactie.html',
            {'tranzactieObj': tranzactieObj}
            )

    def __str__(self):
        return 'Tranzactie'


class undo_redo:
    undo = []
    redo = []
