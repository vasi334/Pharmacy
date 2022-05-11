from django.urls import path
from . import views
from .models import Medicament, Card_client, Tranzactie


urlpatterns = [
    path('', views.projects, name='projects'),
    path('project/<str:pk>/', Medicament.project, name='project'),
    path('carduri/<str:pk>/', Card_client.carduri, name='carduri'),
    path('tranzactii/<str:pk>/', Tranzactie.tranzactii, name='tranzactii'),
    path('cautare-text/', views.cautare_full_text, name='cautare-full-text'),
    path('functionalitati/', views.functionalitati, name='functionalitati'),
    path('generare-random/', views.insert_random, name='generare_random'),
    path('stergere-cascada/', views.stergere_cascada, name='stergere_cascada'),
    path('undo-redo/', views.undo_redo_function, name='undo_redo'),
    path(
        'reduceri-obtinute/',
        views.reduceri_obtinute,
        name='reduceri_obtinute'
        ),
    path(
        'afisare-interval-data/',
        views.interval_data,
        name='afisare_interval_data'),
    path(
        'sterge-tranzactie-interval/',
        views.sterge_tranzactie_interval,
        name='sterge_tranzactie_interval'),
    path('afisare-tuturor/', views.afisarea_tuturor, name='afisarea_tuturor'),
    path(
        'afisare-descrescator/',
        views.afisare_descrescator,
        name='afisare_descrescator'),
    path('scumpire/', views.scumpire, name='scumpire'),

    # Create
    path('createMedicament/', views.createMedicament, name="createMedicament"),
    path('createCard/', views.createCard, name="createCard"),
    path('createTranzactie/', views.createTranzactie, name="createTranzactie"),

    # Update
    path(
        'update-medicament/<str:pk>/',
        views.updateMedicament,
        name="update-medicament"),
    path(
        'update-card/<str:pk>/',
        views.updateCard,
        name="update-card"),
    path(
        'update-tranzactie/<str:pk>/',
        views.updateTranzactie,
        name="update-tranzactie"),

    # Delete
    path(
        'delete-medicament/<str:pk>/',
        views.deleteMedicament,
        name="delete-medicament"),
    path(
        'delete-card/<str:pk>/',
        views.deleteCard,
        name="delete-card"),
    path(
        'delete-tranzactie/<str:pk>/',
        views.deleteTranzactie,
        name="delete-tranzactie"),
]
