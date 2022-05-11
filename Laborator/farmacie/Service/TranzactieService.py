from django.db.models import F
from django.shortcuts import render, redirect
from django.contrib import messages
from farmacie.models import Tranzactie, Medicament, Card_client, undo_redo
from farmacie.forms import TranzactieForm


def createTranzactieService(request):
    form = TranzactieForm()

    if request.method == 'POST':
        form = TranzactieForm(request.POST)
        if Medicament.objects.filter(nume=form['medicament'].value()).exists():
            medicament = Medicament.objects.filter(
                nume=form['medicament'].value()
                )
            if (Card_client.objects.filter(CNP=form['id_card_client'].value())
                    .exists() or form['id_card_client'].value() == ''):
                if (form['nr_bucati'].value() is not None and
                        int(form['nr_bucati'].value()) > 0):
                    if form.is_valid():
                        medicament.update(
                                nr_vanzari=F('nr_vanzari') +
                                int(form['nr_bucati'].value())
                                )
                        form.save()
                        if (Card_client.objects.filter(
                            CNP=form['id_card_client'].value()
                            )
                                .exists()):
                            if medicament[0].necesita_reteta:
                                pret_nou = "{:.2f}".format(
                                    medicament[0].pret -
                                    medicament[0].pret*0.15
                                )
                                messages.success(
                                    request,
                                    f'Tranzactia a fost adaugata cu succes! \
                                        A fost aplicata o reducere de 15%. \
                                        Dupa reducere, pretul este \
                                                de {pret_nou} lei.'
                                    )
                            else:
                                pret_nou = "{:.2f}".format(
                                    medicament[0].pret -
                                    medicament[0].pret*0.1
                                )
                                messages.success(
                                    request,
                                    f'Tranzactia a fost adaugata cu succes! \
                                        A fost aplicata o reducere de 10%. \
                                        Dupa reducere, pretul este \
                                        de {pret_nou} lei.'
                                    )
                        return redirect('projects')
                else:
                    messages.error(
                        request,
                        'Verifica numarul de bucati. Acesta trebuie sa\
                            fie un numar intreg (mai mare decat 0).'
                        )
            else:
                messages.error(
                    request,
                    'Verifica CNP-ul. Acesta trebuie sa contina 13 cifre\
                        si sa fie unic.'
                    )
        else:
            messages.error(
                request,
                'Numele acestui medicament nu exista. Atentie:\
                    numele medicamentului trebuie sa inceapa cu litera mare!'
                )

    context = {'form': form}
    return render(request, 'farmacie/create_tranzactie_form.html', context)


def updateTranzactieService(request, pk):
    tranzactie = Tranzactie.objects.get(id=pk)
    form = TranzactieForm(instance=tranzactie)
    bucati_inainte = int(form['nr_bucati'].value())

    if request.method == 'POST':
        form = TranzactieForm(request.POST, instance=tranzactie)
        if (form['id_card_client'].value() == '' or
                Card_client.objects.filter(
                    CNP=form['id_card_client'].value()).exists()):
            if Medicament.objects.filter(
                nume=form['medicament'].value()
                    ).exists():
                if (form['nr_bucati'].value() is not None and
                        int(form['nr_bucati'].value()) > 0):
                    if bucati_inainte > int(form['nr_bucati'].value()):
                        scadere = bucati_inainte - \
                            int(form['nr_bucati'].value())
                        Medicament.objects.filter(
                            nume=form['medicament'].value()
                            ).update(
                                nr_vanzari=F('nr_vanzari') - scadere
                                )
                    else:
                        adunare = int(form['nr_bucati'].value()) - \
                            bucati_inainte
                        Medicament.objects.filter(
                            nume=form['medicament'].value()
                            ).update(
                                nr_vanzari=F('nr_vanzari') + adunare
                                )
                    if form.is_valid():
                        form.save()
                        messages.success(
                            request,
                            'Tranzactia a fost modificata cu succes!'
                            )
                        return redirect('projects')
                else:
                    messages.error(
                        request,
                        'Numarul de bucati trebuie sa fie \
                            un numar mai mare decat 0.'
                        )
            else:
                messages.error(
                    request,
                    'Numele medicamentului introdus nu exista.'
                    )
        else:
            messages.error(
                request,
                'ID-ul cardului este incorect.'
                )

    context = {'form': form}
    return render(request, 'farmacie/create_tranzactie_form.html', context)


def deleteTranzactieService(request, pk):
    tranzactie = Tranzactie.objects.get(id=pk)
    if request.method == 'POST':
        tranzactie.delete()
        messages.success(
            request,
            'Tranzactia a fost stearsa cu succes!'
            )
        return redirect('projects')
    context = {'tranzactie': tranzactie}
    return render(request, 'farmacie/delete_tranzactie.html', context)


def interval_data_service(request):
    if request.method == 'POST':
        data_0 = request.POST.get('data_0')
        data_0 = data_0[0] + data_0[1] + data_0[2] + data_0[3] + data_0[4] + \
            data_0[5] + data_0[6] + data_0[7] + data_0[8] + data_0[9]

        data_1 = request.POST.get('data_1')
        data_1 = data_1[0] + data_1[1] + data_1[2] + data_1[3] + data_1[4] + \
            data_1[5] + data_1[6] + data_1[7] + data_1[8] + data_1[9]

        tranzactie = Tranzactie.objects.filter(data__range=[data_0, data_1])

        return render(
            request,
            'farmacie/afisare_interval_data.html',
            {'tranzactie': tranzactie})

    return render(request, 'farmacie/afisare_interval_data.html')


def sterge_tranzactie_interval_service(request):
    if request.method == 'POST':
        data_0 = request.POST.get('data_0')
        data_0 = data_0[0] + data_0[1] + data_0[2] + data_0[3] + data_0[4] + \
            data_0[5] + data_0[6] + data_0[7] + data_0[8] + data_0[9]

        data_1 = request.POST.get('data_1')
        data_1 = data_1[0] + data_1[1] + data_1[2] + data_1[3] + data_1[4] + \
            data_1[5] + data_1[6] + data_1[7] + data_1[8] + data_1[9]

        tranzactie = Tranzactie.objects.filter(data__range=[data_0, data_1])
        undo_redo.undo.append([
                'stergere-tranzactii-interval'
            ])
        for t in tranzactie:
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
            'Tranzactiile au fost sterse cu succes!'
            )
    return render(request, 'farmacie/sterge_tranzactie_interval.html')
