from farmacie.api.viewsets import (
    MedicamentViewSet,
    CardViewSet,
    TranzactieViewSet
)
from rest_framework import routers

router = routers.DefaultRouter()
router.register('medicamente', MedicamentViewSet, basename='medicament')
router.register('carduri', CardViewSet, basename='card')
router.register('tranzactii', TranzactieViewSet, basename='tranzactie')
