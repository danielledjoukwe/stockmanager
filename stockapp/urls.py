from django.urls import path
from .views import *


urlpatterns = [
    path('', tableau_de_bord, name='tableau_de_bord'),
    path('produits/', liste_produits, name='liste_produits'),
    path('produits/ajouter/', ajouter_produit, name='ajouter_produit'),
    # path('produits/modifier/', modifier_produit, name='modifier_produit'),
    # path('produits/supprimer/', supprimer_produit, name='supprimer_produit'),

    path('categories/', liste_categories, name='liste_categories'),

    path('ventes/', liste_ventes, name='liste_ventes'),

    path('commandes/', liste_commandes, name='liste_commandes'),

]