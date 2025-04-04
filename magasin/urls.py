from django.urls import path
from .views import *

urlpatterns = [
    path('', tableau_bord_magasin, name='tableau_bord_magasin'),
    path('magasin_produits/', magasin_liste_produits, name='magasin_liste_produits'),
    path('magasin_produits/ajouter/', magasin_ajouter_produit, name='magasin_ajouter_produit'),
    path('magasin_produits/modifier/', magasin_ajouter_produit, name='magasin_modifier_produit'),
    path('magasin_produits/supprimer/', magasin_ajouter_produit, name='magasin_supprimer_produit'),

    path('magasin_categories/', magasin_liste_categories, name='magasin_liste_categories'),

]
