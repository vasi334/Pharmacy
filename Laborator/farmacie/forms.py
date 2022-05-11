from django import forms
from django.forms import ModelForm
from .models import Medicament, Card_client, Tranzactie


class DateInput(forms.DateInput):
    input_type = 'date'


class TimePickerInput(forms.TimeInput):
    input_type = 'time'


class MedicamentForm(ModelForm):
    class Meta:
        model = Medicament
        fields = ['nume', 'producator', 'pret', 'necesita_reteta']

    def __init__(self, *args, **kwargs):
        super(MedicamentForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class CardForm(ModelForm):
    class Meta:
        model = Card_client
        fields = '__all__'
        widgets = {
            'data_nasterii': DateInput(),
            'data_inregistrarii': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        super(CardForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class TranzactieForm(ModelForm):
    class Meta:
        model = Tranzactie
        fields = '__all__'
        widgets = {
            'data': DateInput(),
            'ora': TimePickerInput(),
        }

    def __init__(self, *args, **kwargs):
        super(TranzactieForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
