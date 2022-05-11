from django.test import SimpleTestCase
from django.urls import reverse, resolve
from farmacie.views import (
    projects,
    cautare_full_text,
    functionalitati,
    insert_random,
    interval_data,
    sterge_tranzactie_interval,
    afisare_descrescator,
    afisarea_tuturor,
    scumpire,
    createMedicament,
    createCard,
    createTranzactie,
    updateMedicament,
    updateCard,
    updateTranzactie,
    deleteMedicament,
    deleteCard,
    deleteTranzactie
)
from farmacie.models import Medicament, Card_client, Tranzactie


class TestUrls(SimpleTestCase):

    def test_list_urls_is_resolves(self):
        url = reverse('projects')
        # print(resolve(url))
        self.assertEquals(resolve(url).func, projects)

    def test_medicament_url_resolves(self):
        url = reverse('project', args=['some-id'])
        self.assertEquals(resolve(url).func, Medicament.project)

    def test_card_url_resolves(self):
        url = reverse('carduri', args=['some-id'])
        self.assertEquals(resolve(url).func, Card_client.carduri)

    def test_tranzactie_url_resolves(self):
        url = reverse('tranzactii', args=['some-id'])
        self.assertEquals(resolve(url).func, Tranzactie.tranzactii)

    def test_cautare_full_text_url_resolves(self):
        url = reverse('cautare-full-text')
        self.assertEquals(resolve(url).func, cautare_full_text)

    def test_functionalitati_url_resolves(self):
        url = reverse('functionalitati')
        self.assertEquals(resolve(url).func, functionalitati)

    def test_generare_random_url_resolves(self):
        url = reverse('generare_random')
        self.assertEquals(resolve(url).func, insert_random)

    def test_afisare_interval_data_url_resolves(self):
        url = reverse('afisare_interval_data')
        self.assertEquals(resolve(url).func, interval_data)

    def test_sterge_tranzactie_interval_url_resolves(self):
        url = reverse('sterge_tranzactie_interval')
        self.assertEquals(resolve(url).func, sterge_tranzactie_interval)

    def test_afisarea_tuturor_url_resolves(self):
        url = reverse('afisarea_tuturor')
        self.assertEquals(resolve(url).func, afisarea_tuturor)

    def test_afisare_descrescator_url_resolves(self):
        url = reverse('afisare_descrescator')
        self.assertEquals(resolve(url).func, afisare_descrescator)

    def test_scumpire_url_resolves(self):
        url = reverse('scumpire')
        self.assertEquals(resolve(url).func, scumpire)

    def test_createMedicament_url_resolves(self):
        url = reverse('createMedicament')
        self.assertEquals(resolve(url).func, createMedicament)

    def test_createCard_url_resolves(self):
        url = reverse('createCard')
        self.assertEquals(resolve(url).func, createCard)

    def test_createTranzactie_url_resolves(self):
        url = reverse('createTranzactie')
        self.assertEquals(resolve(url).func, createTranzactie)

    def test_update_medicament_url_resolves(self):
        url = reverse('update-medicament', args=['some-id'])
        self.assertEquals(resolve(url).func, updateMedicament)

    def test_update_card_url_resolves(self):
        url = reverse('update-card', args=['some-id'])
        self.assertEquals(resolve(url).func, updateCard)

    def test_update_tranzactie_url_resolves(self):
        url = reverse('update-tranzactie', args=['some-id'])
        self.assertEquals(resolve(url).func, updateTranzactie)

    def test_delete_medicament_url_resolves(self):
        url = reverse('delete-medicament', args=['some-id'])
        self.assertEquals(resolve(url).func, deleteMedicament)

    def test_delete_card_url_resolves(self):
        url = reverse('delete-card', args=['some-id'])
        self.assertEquals(resolve(url).func, deleteCard)

    def test_delete_tranzactie_url_resolves(self):
        url = reverse('delete-tranzactie', args=['some-id'])
        self.assertEquals(resolve(url).func, deleteTranzactie)
