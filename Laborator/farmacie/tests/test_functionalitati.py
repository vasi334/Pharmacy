from django.test import Client
from django.test import TestCase
from farmacie.models import Card_client, Medicament, Tranzactie
from farmacie.views import sterge_tranzactie_interval


class TestMedicamentFunctionalitati(TestCase):
    def setUp(self):
        self.medicament_1 = Medicament.objects.create(
            nume='Medicament 1',
            producator='SaS',
            pret=6,
            necesita_reteta=True
        )
        self.medicament_2 = Medicament.objects.create(
            nume='Medicament 2',
            producator='CCC',
            pret=4,
            necesita_reteta=False
        )


class TestCardFunctionalitati(TestCase):
    def setUp(self):
        self.card_1 = Card_client.objects.create(
            nume='Horoi',
            prenume='Vasile',
            CNP=1234567891012,
            data_nasterii='2000-10-16',
            data_inregistrarii='2020-12-10'
        )
        self.card_2 = Card_client.objects.create(
            nume='Horoi',
            prenume='Alina',
            CNP=1234567891011,
            data_nasterii='2001-11-24',
            data_inregistrarii='2020-12-15'
        )


class TestTranzactieFunctionalitati(TestCase):
    def setUp(self):
        self.c = Client()
        self.tranzactie_1 = Tranzactie.objects.create(
            id_card_client=1414141414141,
            medicament='Paracetamol',
            nr_bucati=4,
            data='2020-12-10',
            ora='16:04'
        )
        self.tranzactie_2 = Tranzactie.objects.create(
            id_card_client=1515151515151,
            medicament='Decasept',
            nr_bucati=5,
            data='2020-10-15',
            ora='19:25'
        )

    def stergere_interval_test(self):
        response = self.c.post(
            '/sterge-tranzactie-interval/',
            {'data_0': '10.12.2019', 'data_1': '12.12.2021'}
        )
        sterge_tranzactie_interval(request=response)
        self.assertEqual(str(self.tranzactie_1.id_card_client), 4)
        self.assertEqual(str(self.tranzactie_1.medicament), None)
        self.assertEqual(str(self.tranzactie_1.nr_bucati), None)
        self.assertEqual(str(self.tranzactie_1.data), None)
        self.assertEqual(str(self.tranzactie_1.ora), None)
