from django.http import JsonResponse
from rest_framework.decorators import action
from farmacie.models import Card_client, Medicament, Tranzactie
from .serializers import (
    MedicamentSerializer,
    CardSerializer,
    TranzactieSerializer
)
from rest_framework import viewsets
from rest_framework.response import Response
from django_filters import rest_framework as filters


class MedicamentFilter(filters.FilterSet):

    class Meta:
        model = Medicament
        fields = {
            'nume': ['icontains'],
            'producator': ['icontains']
        }


class CardFilter(filters.FilterSet):

    class Meta:
        model = Card_client
        fields = {
            'nume': ['icontains'],
            'prenume': ['icontains']
        }


class TranzactieFilter(filters.FilterSet):

    class Meta:
        model = Tranzactie
        fields = {
            'id_card_client': ['icontains'],
            'medicament': ['icontains']
        }


class MedicamentViewSet(viewsets.ModelViewSet):

    queryset = Medicament.objects.all()
    serializer_class = MedicamentSerializer
    filterset_class = MedicamentFilter

    @action(methods=['get'], detail=False)
    def newest(self, request):
        newest = self.get_queryset().order_by('nume').last()
        serializer = self.get_serializer_class()(newest)
        return Response(serializer.data)

    @action(methods=['delete'], detail=False)
    def delete(self, request):
        Medicament.objects.all().delete()
        return JsonResponse(
            {'message':
                'Medicamentele au fost sterse cu succes!'}
        )


class CardViewSet(viewsets.ModelViewSet):

    queryset = Card_client.objects.all()
    serializer_class = CardSerializer
    filterset_class = CardFilter

    @action(methods=['get'], detail=False)
    def newest(self, request):
        newest = self.get_queryset().order_by('nume').last()
        serializer = self.get_serializer_class()(newest)
        return Response(serializer.data)

    @action(methods=['delete'], detail=False)
    def delete(self, request):
        Card_client.objects.all().delete()
        return JsonResponse(
            {'message':
                'Cardurile au fost sterse cu succes!'}
        )


class TranzactieViewSet(viewsets.ModelViewSet):

    queryset = Tranzactie.objects.all()
    serializer_class = TranzactieSerializer
    filterset_class = TranzactieFilter

    @action(methods=['get'], detail=False)
    def newest(self, request):
        newest = self.get_queryset().order_by('id_card_client').last()
        serializer = self.get_serializer_class()(newest)
        return Response(serializer.data)

    @action(methods=['delete'], detail=False)
    def delete(self, request):
        Tranzactie.objects.all().delete()
        return JsonResponse(
            {'message':
                'Tranzactiile au fost sterse cu succes!'}
        )
