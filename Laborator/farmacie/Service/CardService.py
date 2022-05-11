from django.shortcuts import render, redirect
from django.contrib import messages
from farmacie.models import Card_client, undo_redo
from farmacie.forms import CardForm


def contine_numar(stringul):
    return any(char.isdigit() for char in stringul)


def createCardService(request):
    form = CardForm()

    if request.method == 'POST':
        form = CardForm(request.POST)
        nume = form['nume'].value()
        prenume = form['prenume'].value()
        if contine_numar(nume) is False and contine_numar(prenume) is False:
            if (Card_client.objects.filter(CNP=form['CNP'].value()).exists()
                    is False):
                if form.is_valid():
                    form.save()
                    card = Card_client.objects.get(
                        nume=form['nume'].value()
                        )
                    undo_redo.undo.append(
                        ['add-card',
                            card.id,
                            card.nume,
                            card.prenume,
                            card.CNP,
                            card.data_nasterii,
                            card.data_inregistrarii])
                    messages.success(
                        request,
                        'Cardul a fost adaugat cu succes!'
                        )
                    return redirect('projects')
            else:
                messages.error(request, 'CNP-ul introdus exista deja.')
        else:
            messages.error(
                request,
                'Numele si prenumele trebuie sa contina doar litere.'
                )

    context = {'form': form}
    return render(request, 'farmacie/create_card_form.html', context)


def updateCardService(request, pk):
    card = Card_client.objects.get(id=pk)
    form = CardForm(instance=card)

    if request.method == 'POST':
        form = CardForm(request.POST, instance=card)
        nume = form['nume'].value()
        prenume = form['prenume'].value()
        if contine_numar(nume) is False and contine_numar(prenume) is False:
            undo_redo.undo.append(
                ['update-card',
                    card.id,
                    card.nume,
                    card.prenume,
                    card.CNP,
                    card.data_nasterii,
                    card.data_inregistrarii])
            if form.is_valid():
                form.save()
                messages.success(
                    request,
                    'Cardul a fost modificat cu succes!'
                    )
                return redirect('projects')
        else:
            messages.error(
                request,
                'Numele si prenumele trebuie sa contina doar litere.'
                )

    context = {'form': form}
    return render(request, 'farmacie/create_card_form.html', context)


def deleteCardService(request, pk):
    card = Card_client.objects.get(id=pk)
    if request.method == 'POST':
        undo_redo.undo.append(
                        ['delete-card',
                            card.id,
                            card.nume,
                            card.prenume,
                            card.CNP,
                            card.data_nasterii,
                            card.data_inregistrarii])
        card.delete()
        messages.success(
            request,
            'Cardul a fost sters cu succes!'
            )
        return redirect('projects')
    context = {'card': card}
    return render(request, 'farmacie/delete_card.html', context)
