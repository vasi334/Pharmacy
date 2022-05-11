from django.test import TestCase
from farmacie.forms import MedicamentForm, CardForm, TranzactieForm


class TestForms(TestCase):

    def test_medicament_form_valid_data(self):
        form = MedicamentForm(data={
            'nume': 'Medicament 1',
            'producator': 'SaS',
            'pret': 6,
            'necesita_reteta': False,
            'nr_vanzari': 4
        }
        )

        self.assertTrue(form.is_valid())

    def test_medicament_form_invalid_data(self):
        form = MedicamentForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)

    def test_card_form_valid_data(self):
        form = CardForm(data={
            'nume': 'Alex',
            'prenume': 'Ceausu',
            'CNP': 1234567891011,
            'data_nasterii': '2000-10-16',
            'data_inregistrarii': '2020-10-16'
        }
        )

        self.assertTrue(form.is_valid())

    def test_card_form_invalid_data(self):
        form = CardForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 5)

    def test_tranzactie_form_valid_data(self):
        form = TranzactieForm(data={
            'id_card_client': 1414141414141,
            'medicament': 'Paracetamol',
            'nr_bucati': 4,
            'data': '2020-12-10',
            'ora': '16:04'
        }
        )

        self.assertTrue(form.is_valid())

    def test_tranzactie_form_invalid_data(self):
        form = TranzactieForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)
