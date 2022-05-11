from rest_framework import serializers
from farmacie.models import Medicament, Card_client, Tranzactie


class MedicamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicament
        fields = '__all__'


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card_client
        fields = '__all__'


class TranzactieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tranzactie
        fields = '__all__'
