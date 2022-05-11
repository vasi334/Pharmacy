from django.test import TestCase, Client
from django.urls import reverse
from farmacie.models import Medicament, Card_client, Tranzactie


class TestMedicamentCRUD(TestCase):

    def setUp(self):
        self.client = Client()
        self.createMedicament_url = reverse('createMedicament')
        self.detail_url = reverse(
            'project',
            args=['597b9134-3d4a-4819-a85b-1bce2dc9f204']
        )
        Medicament.objects.create(
            id='597b9134-3d4a-4819-a85b-1bce2dc9f204',
            nume='Medicament 1',
            producator='SAS',
            pret=6,
            necesita_reteta=True
        )

    def test_medicament_list_GET(self):
        response = self.client.get(self.createMedicament_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'farmacie/create_medicament_form.html'
        )

    def test_medicament_detail_GET(self):
        response = self.client.get(self.detail_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'farmacie/single-project.html'
        )

    def test_medicament_detail_POST(self):
        self.medicament_vechi = Medicament.objects.create(
            id='a3ffb6e2-0005-4756-aea8-af30facb423a',
            nume='M1',
            producator='SAS',
            pret=6,
            necesita_reteta=True
        )
        response = self.client.post(
            reverse(
                'update-medicament',
                args=['a3ffb6e2-0005-4756-aea8-af30facb423a']
            ),
            {
                'nume': 'M2',
                'producator': 'Cas',
                'pret': 8,
                'necesita_reteta': False
            })
        self.assertEquals(response.status_code, 200)
        self.medicament_vechi.refresh_from_db()
        self.assertEquals(self.medicament_vechi.nume, 'M1')
        self.assertEquals(self.medicament_vechi.necesita_reteta, True)


class TestCardCRUD(TestCase):

    def setUp(self):
        self.client = Client()
        self.createCard_url = reverse('createCard')
        self.detail_url = reverse(
            'carduri',
            args=['be400e76-f005-412f-964f-6415f63c055f']
        )
        Card_client.objects.create(
            id='be400e76-f005-412f-964f-6415f63c055f',
            nume='Aaron',
            prenume='Kosminski',
            CNP='1234567895551',
            data_nasterii='2000-10-16',
            data_inregistrarii='2020-12-10'
        )

    def test_card_list_GET(self):
        response = self.client.get(self.createCard_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'farmacie/create_card_form.html'
        )

    def test_card_detail_GET(self):
        response = self.client.get(self.detail_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'farmacie/single-card.html'
        )

    def test_card_detail_POST(self):
        self.card_vechi = Card_client.objects.create(
            id='ac7c6894-a63f-437a-8eb7-b7ef49fbfc0b',
            nume='Aaron',
            prenume='Kosminski',
            CNP=1234567891011,
            data_nasterii='2000-10-16',
            data_inregistrarii='2020-12-10'
        )
        response = self.client.post(
            reverse(
                'update-card',
                args=['ac7c6894-a63f-437a-8eb7-b7ef49fbfc0b']
            ),
            {
                'nume': 'Horoi',
                'prenume': 'Vasile',
                'CNP': '1234567891021',
                'data_nasterii': '2000-10-16',
                'data_inregistrarii': '2020-12-10'
            })
        self.assertEquals(response.status_code, 302)
        self.card_vechi.refresh_from_db()
        self.assertEquals(self.card_vechi.nume, 'Horoi')
        self.assertEquals(self.card_vechi.prenume, 'Vasile')


class TestTranzactieCRUD(TestCase):

    def setUp(self):
        self.client = Client()
        self.createTranzactie_url = reverse('createTranzactie')
        self.detail_url = reverse(
            'tranzactii',
            args=['2c411709-3c4e-4b29-9965-6fd888658dfe']
        )
        Tranzactie.objects.create(
            id='2c411709-3c4e-4b29-9965-6fd888658dfe',
            id_card_client='1234567891231',
            medicament='Medicament 1',
            nr_bucati=4,
            data='2020-12-10',
            ora='16:04'
        )

    def test_tranzactie_list_GET(self):
        response = self.client.get(self.createTranzactie_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'farmacie/create_tranzactie_form.html'
        )

    def test_tranzactie_detail_GET(self):
        response = self.client.get(self.detail_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'farmacie/single-tranzactie.html'
        )
