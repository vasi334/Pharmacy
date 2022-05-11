from django.contrib import admin
from .models import Card_client, Tranzactie, Medicament


# Register your models here.
admin.site.register(Medicament)
admin.site.register(Card_client)
admin.site.register(Tranzactie)
