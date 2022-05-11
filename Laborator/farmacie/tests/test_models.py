from farmacie.models import Card_client, Medicament, Tranzactie
from django.test import TestCase


class TestMedicamentModels(TestCase):

    def setUp(self):
        self.medicament = Medicament.objects.create(
            nume='Medicament 1',
            producator='SaS',
            pret=6,
            necesita_reteta=True
        )

    def test_medicament_str(self):
        self.assertEqual(str(self.medicament.nume), 'Medicament 1')
        self.assertEqual(str(self.medicament.producator), 'SaS')
        self.assertEqual(str(self.medicament.pret), '6')
        self.assertEqual(str(self.medicament.necesita_reteta), 'True')


class TestCardModels(TestCase):

    def setUp(self):
        self.card = Card_client.objects.create(
            nume='Alex',
            prenume='Ceausu',
            CNP=1234567891011,
            data_nasterii='2000-10-16',
            data_inregistrarii='2020-12-10'
        )

    def test_card_str(self):
        self.assertEqual(str(self.card.nume), 'Alex')
        self.assertEqual(str(self.card.prenume), 'Ceausu')
        self.assertEqual(str(self.card.CNP), '1234567891011')
        self.assertEqual(str(self.card.data_nasterii), '2000-10-16')
        self.assertEqual(str(self.card.data_inregistrarii), '2020-12-10')


class TestTranzactieModels(TestCase):

    def setUp(self):
        self.tranzactie = Tranzactie.objects.create(
            id_card_client=1414141414141,
            medicament='Paracetamol',
            nr_bucati=4,
            data='2020-12-10',
            ora='16:04'
        )

    def test_tranzactie_str(self):
        self.assertEqual(str(self.tranzactie.id_card_client), '1414141414141')
        self.assertEqual(str(self.tranzactie.medicament), 'Paracetamol')
        self.assertEqual(str(self.tranzactie.nr_bucati), '4')
        self.assertEqual(str(self.tranzactie.data), '2020-12-10')
        self.assertEqual(str(self.tranzactie.ora), '16:04')
