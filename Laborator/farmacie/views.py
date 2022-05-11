from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render
from .models import Medicament, Card_client, Tranzactie, undo_redo
# from django.http import HttpResponse
from farmacie.Service.CardService import (
    createCardService,
    deleteCardService,
    updateCardService
)
from farmacie.Service.TranzactieService import (
    createTranzactieService,
    deleteTranzactieService,
    interval_data_service,
    sterge_tranzactie_interval_service,
    updateTranzactieService
)
from farmacie.Service.MedicamentService import (
    createMedicamentService,
    updateMedicamentService,
    deleteMedicamentService,
    insert_random_service,
    afisare_descrescator_service,
    scumpire_service,
    stergere_cascada_medicament
)
import operator


def projects(request):
    medicamente = Medicament.objects.all()
    carduri = Card_client.objects.all()
    tranzactii = Tranzactie.objects.all()
    context = {
        'medicamente': medicamente,
        'carduri': carduri,
        'tranzactii': tranzactii}
    return render(request, 'farmacie/projects.html', context)


def cautare_full_text(request):
    if request.method == 'POST':
        cautat = request.POST['cautat']

        queryset = Medicament.objects.filter(
            Q(nume__contains=cautat) |
            Q(producator__contains=cautat) |
            Q(pret__contains=cautat))

        queryset1 = Card_client.objects.filter(
            Q(nume__contains=cautat) |
            Q(prenume__contains=cautat) |
            Q(CNP__contains=cautat) |
            Q(data_inregistrarii__contains=cautat) |
            Q(data_nasterii__contains=cautat))

        queryset2 = Tranzactie.objects.filter(
            Q(id_card_client__contains=cautat) |
            Q(nr_bucati__contains=cautat) |
            Q(data__contains=cautat) |
            Q(ora__contains=cautat))

        return render(request, 'farmacie/cautare_text.html', {
            'queryset': queryset,
            'queryset1': queryset1,
            'queryset2': queryset2})


# CRUD #


def createMedicament(request):
    return createMedicamentService(request=request)


def updateMedicament(request, pk):
    return updateMedicamentService(request=request, pk=pk)


def deleteMedicament(request, pk):
    return deleteMedicamentService(request=request, pk=pk)


def createCard(request):
    return createCardService(request=request)


def updateCard(request, pk):
    return updateCardService(request=request, pk=pk)


def deleteCard(request, pk):
    return deleteCardService(request=request, pk=pk)


def createTranzactie(request):
    return createTranzactieService(request=request)


def updateTranzactie(request, pk):
    return updateTranzactieService(request=request, pk=pk)


def deleteTranzactie(request, pk):
    return deleteTranzactieService(request=request, pk=pk)


# Functionalitati


def insert_random(request):
    return insert_random_service(request=request)


def functionalitati(request):
    return render(request, 'farmacie/functionalitati.html')


def interval_data(request):
    return interval_data_service(request=request)


def sterge_tranzactie_interval(request):
    return sterge_tranzactie_interval_service(request=request)


def afisare_descrescator(request):
    return afisare_descrescator_service(request=request)


def scumpire(request):
    return scumpire_service(request=request)


def afisarea_tuturor(request):
    rez = Medicament.objects.all()
    rez1 = Card_client.objects.all()
    rez2 = Tranzactie.objects.all()
    context = {'rez': rez, 'rez1': rez1, 'rez2': rez2}

    return render(request, 'farmacie/afisarea_tuturor.html', context)


def stergere_cascada(request):
    return stergere_cascada_medicament(request=request)


def reduceri_obtinute(request):
    d = dict()

    for card in Card_client.objects.all():
        d[card.CNP] = 0

    for card in Card_client.objects.all():
        for tranzactie in Tranzactie.objects.all():
            medicament = Medicament.objects.get(nume=tranzactie.medicament)
            if (card.CNP == tranzactie.id_card_client and
                    medicament.necesita_reteta is True):
                d[card.CNP] += medicament.pret*(15/100)
            elif (card.CNP == tranzactie.id_card_client and
                    medicament.necesita_reteta is False):
                d[card.CNP] += medicament.pret*(10/100)

    sorted_d = dict(
        sorted(
            d.items(),
            key=operator.itemgetter(1),
            reverse=True
            )
        )
    queryset = [str(key) for key in sorted_d]

    carduri = Card_client.objects.all()
    context = {'queryset': queryset, 'carduri': carduri}

    return render(request, 'farmacie/reduceri_obtinute.html', context)


def undo_redo_function(request):
    if request.method == 'POST' and 'undo' in request.POST:
        if undo_redo.undo:
            operatie = undo_redo.undo.pop()
            if operatie[0] == 'add-med':
                medicament = Medicament.objects.get(id=operatie[1])
                undo_redo.redo.append([
                    'add-med-undo',
                    medicament.id,
                    medicament.nume,
                    medicament.producator,
                    medicament.pret,
                    medicament.necesita_reteta,
                ])
                medicament.delete()
            elif operatie[0] == 'update-med':
                medicament = Medicament.objects.get(id=operatie[1])
                undo_redo.redo.append([
                    'update-med-undo',
                    medicament.id,
                    medicament.nume,
                    medicament.producator,
                    medicament.pret,
                    medicament.necesita_reteta
                ])
                medicament.nume = operatie[2]
                medicament.producator = operatie[3]
                medicament.pret = operatie[4]
                medicament.necesita_reteta = operatie[5]
                medicament.save()
            elif operatie[0] == 'delete-med':
                Medicament.objects.create(
                    id=operatie[1],
                    nume=operatie[2],
                    producator=operatie[3],
                    pret=operatie[4],
                    necesita_reteta=operatie[5]
                )
                undo_redo.redo.append([
                    'delete-med-undo',
                    operatie[1]
                ])
            elif operatie[0] == 'add-card':
                card = Card_client.objects.get(id=operatie[1]).delete()
                undo_redo.redo.append([
                    'add-card-undo',
                    card.id,
                    card.nume,
                    card.prenume,
                    card.CNP,
                    card.data_nasterii,
                    card.data_inregistrarii
                ])
                card.delete()
            elif operatie[0] == 'update-card':
                card = Card_client.objects.get(id=operatie[1])
                undo_redo.redo.append([
                    'update-card-undo',
                    card.id,
                    card.nume,
                    card.prenume,
                    card.CNP,
                    card.data_nasterii,
                    card.data_inregistrarii
                ])
                card.nume = operatie[2]
                card.prenume = operatie[3]
                card.CNP = operatie[4]
                card.data_nasterii = operatie[5]
                card.data_inregistrarii = operatie[6]
                card.save()
            elif operatie[0] == 'delete-card':
                Card_client.objects.create(
                    id=operatie[1],
                    nume=operatie[2],
                    prenume=operatie[3],
                    CNP=operatie[4],
                    data_nasterii=operatie[5],
                    data_inregistrarii=operatie[6]
                )
                undo_redo.redo.append([
                    'delete-card-undo',
                    operatie[1]
                ])
            elif operatie[0] == 'scumpire-med':
                for medicament in operatie[2]:
                    medicament.pret = medicament.pret/float('1.' + operatie[1])
                    medicament.save()
            elif operatie[0] == 'stergere-tranzactii-interval':
                undo_redo.redo.append([
                    'stergere-tranzactii-interval-undo'])
                for tranzactie in operatie[1:]:
                    Tranzactie.objects.create(
                        id=tranzactie[0],
                        id_card_client=tranzactie[1],
                        medicament=tranzactie[2],
                        nr_bucati=tranzactie[3],
                        data=tranzactie[4],
                        ora=tranzactie[5]
                    )
                    undo_redo.redo[-1].append([
                        tranzactie[0]
                    ]
                    )
            messages.success(
                request,
                'Undo a fost efectuat cu succes!')
        else:
            messages.error(
                    request,
                    'Nu exista operatii pentru a face undo!'
                    )
    elif request.method == 'POST' and 'redo' in request.POST:
        if undo_redo.redo:
            operatie = undo_redo.redo.pop()
            if operatie[0] == 'add-med-undo':
                Medicament.objects.create(
                    id=operatie[1],
                    nume=operatie[2],
                    producator=operatie[3],
                    pret=operatie[4],
                    necesita_reteta=operatie[5]
                )
                undo_redo.undo.append([
                    'add-med',
                    operatie[1]
                ])
            elif operatie[0] == 'update-med-undo':
                medicament = Medicament.objects.get(id=operatie[1])
                undo_redo.undo.append([
                    'update-med',
                    medicament.id,
                    medicament.nume,
                    medicament.producator,
                    medicament.pret,
                    medicament.necesita_reteta
                ])
                medicament.nume = operatie[2]
                medicament.producator = operatie[3]
                medicament.pret = operatie[4]
                medicament.necesita_reteta = operatie[5]
                medicament.save()
            elif operatie[0] == 'delete-med-undo':
                medicament = Medicament.objects.get(id=operatie[1])
                undo_redo.undo.append([
                    'delete-med',
                    medicament.id,
                    medicament.nume,
                    medicament.producator,
                    medicament.pret,
                    medicament.necesita_reteta
                ])
                medicament.delete()
            elif operatie[0] == 'add-card-undo':
                Card_client.objects.create(
                    id=operatie[1],
                    nume=operatie[2],
                    prenume=operatie[3],
                    CNP=operatie[4],
                    data_nasterii=operatie[5],
                    data_inregistrarii=operatie[6]
                )
                undo_redo.undo.append([
                    'add-card',
                    operatie[1]
                ])
            elif operatie[0] == 'update-card-undo':
                card = Card_client.objects.get(id=operatie[1])
                undo_redo.undo.append([
                    'update-card',
                    card.id,
                    card.nume,
                    card.prenume,
                    card.CNP,
                    card.data_nasterii,
                    card.data_inregistrarii
                ])
                card.nume = operatie[2]
                card.prenume = operatie[3]
                card.CNP = operatie[4]
                card.data_nasterii = operatie[5]
                card.data_inregistrarii = operatie[6]
                card.save()
            elif operatie[0] == 'delete-card-undo':
                card = Card_client.objects.get(id=operatie[1])
                undo_redo.undo.append([
                    'delete-med',
                    card.id,
                    card.nume,
                    card.prenume,
                    card.CNP,
                    card.data_nasterii,
                    card.data_inregistrarii
                ])
                card.delete()
            elif operatie[0] == 'stergere-tranzactii-interval-undo':
                undo_redo.undo.append([
                    'stergere-tranzactii-interval'
                    ])
                for tranzactie in operatie[1:]:
                    t = Tranzactie.objects.get(id=tranzactie[0])
                    undo_redo.undo[-1].append([
                        t.id,
                        t.id_card_client,
                        t.medicament,
                        t.nr_bucati,
                        t.data,
                        t.ora
                    ])
                    t.delete()
            messages.success(
                request,
                'Redo a fost efectuat cu succes!')
        else:
            messages.error(
                    request,
                    'Nu exista operatii pentru a face redo!'
                    )
    return render(request, 'farmacie/undo_redo.html')
