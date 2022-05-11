from django.db.models import F
from django.shortcuts import render, redirect
from django.contrib import messages
from farmacie.models import Medicament, Tranzactie, undo_redo
from farmacie.forms import MedicamentForm
import random


def createMedicamentService(request):
    form = MedicamentForm()

    if request.method == 'POST' and 'submit' in request.POST:
        form = MedicamentForm(request.POST)
        if (Medicament.objects.filter(nume=form['nume'].value()).exists()
                is False):
            if (form['pret'].value() is not None and
                    float(form['pret'].value()) > 0):
                if form.is_valid():
                    form.save()
                    medicament = Medicament.objects.get(
                        nume=form['nume'].value()
                        )
                    undo_redo.undo.append(
                        ['add-med',
                            medicament.id,
                            medicament.nume,
                            medicament.producator,
                            medicament.pret,
                            medicament.necesita_reteta])
                    messages.success(
                        request,
                        'Medicamentul a fost adaugat cu succes!'
                        )
                    return redirect('projects')
            else:
                messages.error(
                    request,
                    'Pretul trebuie sa fie mai mare decat 0.'
                )
        else:
            messages.error(request, 'Numele medicamentului exista deja.')

    context = {'form': form}
    return render(request, 'farmacie/create_medicament_form.html', context)


def updateMedicamentService(request, pk):
    medicament = Medicament.objects.get(id=pk)
    form = MedicamentForm(instance=medicament)
    numele = form['nume'].value()

    if request.method == 'POST' and 'submit' in request.POST:
        form = MedicamentForm(request.POST, instance=medicament)
        if (numele == form['nume'].value() or
                Medicament.objects.filter(nume=form['nume'].value()).exists()
                is False):
            if (form['pret'].value() is not None and
                    float(form['pret'].value()) > 0):
                undo_redo.undo.append(
                        ['update-med',
                            medicament.id,
                            medicament.nume,
                            medicament.producator,
                            medicament.pret,
                            medicament.necesita_reteta])
                if form.is_valid():
                    form.save()
                    messages.success(
                        request,
                        'Medicamentul a fost modificat cu succes!'
                        )
                    return redirect('projects')
            else:
                messages.error(
                    request,
                    'Pretul trebuie sa fie mai mare decat 0.'
                    )
        else:
            messages.error(request, 'Numele medicamentului exista deja.')
    elif request.method == 'POST' and 'undo' in request.POST:
        form = MedicamentForm(instance=medicament)

    context = {'form': form}
    return render(request, 'farmacie/create_medicament_form.html', context)


def deleteMedicamentService(request, pk):
    medicament = Medicament.objects.get(id=pk)
    if request.method == 'POST':
        undo_redo.undo.append(
                        ['delete-med',
                            medicament.id,
                            medicament.nume,
                            medicament.producator,
                            medicament.pret,
                            medicament.necesita_reteta])
        medicament.delete()
        messages.success(
            request,
            'Medicamentul a fost sters cu succes!'
            )
        return redirect('projects')
    context = {'medicament': medicament}
    return render(request, 'farmacie/delete_template.html', context)


def insert_random_service(request):
    # id, nume, producător, preț, necesită rețetă. Prețul să fie strict pozitiv

    if request.method == 'POST':
        n = request.POST['random']
        n = int(n)
        for j in range(n):
            nume = ['Kapa', 'Ese', 'Bur', 'Meta', 'Cave', 'Sit', 'Vool']
            producator = ['SAs', 'CuP', 'NoV', 'DeS', 'PiX', 'NOi', 'SuuV']
            pret = [3.7, 4.5, 6.7, 8.9, 1.0, 2.3, 4.1]
            necesita_reteta = [True, False]
            nume_random = random.choice(nume)
            producator_random = random.choice(producator)
            pret_random = random.choice(pret)
            necesita_reteta_random = random.choice(necesita_reteta)
            i = Medicament(
                nume=nume_random,
                producator=producator_random,
                pret=pret_random,
                necesita_reteta=necesita_reteta_random)
            i.save()
        messages.success(
            request,
            'Medicamentele au fost adaugate cu succes!'
            )

    return render(request, 'farmacie/generare_random.html')


def afisare_descrescator_service(request):
    medicamente = Medicament.objects.all().order_by('-nr_vanzari')
    return render(
        request,
        'farmacie/afisare_descrescator.html',
        {'medicamente': medicamente}
        )


def scumpire_service(request):
    if request.method == 'POST':
        procentaj = request.POST['procentaj']
        valoare = request.POST['valoare']
        medicamente = Medicament.objects.filter(pret__lt=int(valoare))
        undo_redo.undo.append(
                        ['scumpire-med',
                            medicamente,
                            procentaj])
        Medicament.objects.filter(
                                pret__lt=int(valoare)
                                ).update(
                                pret=F('pret') + int(procentaj)/100*F('pret')
                                )
        messages.success(
            request,
            'Scumpirea a fost efectuata cu succes!'
            )

    return render(request, 'farmacie/scumpire.html')


def stergere_cascada_medicament(request):
    if request.method == 'POST':
        medicament_sters = request.POST['medicament']
        if Medicament.objects.filter(nume=medicament_sters):
            Tranzactie.objects.filter(
                medicament=medicament_sters
            ).delete()
            Medicament.objects.filter(nume=medicament_sters).delete()
        else:
            messages.error(request, 'Numele medicamentului nu exista. \
                Atentie: acesta trebuie sa inceapa cu litera mare!')
    return render(request, 'farmacie/stergere_cascada.html')
