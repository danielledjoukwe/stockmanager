from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Count, F, Q
from django.utils import timezone
from datetime import timedelta
from .models import Produit
# , Categorie, ventes, Commandes
# from .forms import ProduitForm, CommandeForm, LigneCommandeForm



def tableau_de_bord(request):
    # # Statistiques générales
    total_produits = Produit.objects.count()    
    
    # # Nouveaux produits ce mois
    debut_mois = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    nouveaux_produits = Produit.objects.filter(date_creation__gte=debut_mois).count()
    
    # # Produits en rupture ou stock faible
    produits_rupture = Produit.objects.filter(quantite=0).count()
    produits_stock_faible = Produit.objects.filter(quantite__gt=0, quantite__lte=F('seuil_alerte')).count()
    
    # # Valeur totale du stock
    valeur_stock = Produit.objects.aggregate(total=Sum(F('prix') * F('quantite')))['total'] or 0
    
    # # Valeur du stock le mois dernier (pour calculer la variation)
    dernier_mois = debut_mois - timedelta(days=1)
    # # Cette logique devrait être adaptée selon vos besoins spécifiques
    variation_stock = 5  # Supposons une augmentation de 5% pour l'exemple
    
    context = {
        'total_produits': total_produits,
        'nouveaux_produits': nouveaux_produits,
        'produits_rupture': produits_rupture,
        'produits_stock_faible': produits_stock_faible,
        'valeur_stock': valeur_stock,
        'variation_stock': variation_stock,
        'produits': Produit.objects.all().order_by('nom')
    }
    
    return render(request, 'tableau_de_bord/tableau_de_bord.html',context)

def magasin(request):

    
    return redirect('bord.html')

def liste_produits(request):

    if request.method == 'POST':
        if "ajouter_produit" in request.POST:
             nom = request.POST['nom_produit']
             prix = request.POST['prix']
             quantite = request.POST['quantite']
             print(nom, prix, quantite)
             

             print("HEllo world")

             
             
        
    

    # produits = Produit.objects.all().order_by('code')
    
    # context = {
    #     'produits': produits
    # }
    
    return render(request, 'tableau_de_bord/produits/liste_produits.html')

def ajouter_produit(request):
    if request.method == 'POST':
        # Get form data
        nom = request.POST.get('nom_produit', '')
        categorie = request.POST.get('add-product-category', '')  # This needs to match the input name
        prix = request.POST.get('Prix', '')
        quantite = request.POST.get('Quantité', '')
        
        # Print the values for testing
        print(f"Nom: {nom}, Catégorie: {categorie}, Prix: {prix}, Quantité: {quantite}")
        
        # Here you would typically create a new product in your database
        # Example: Produit.objects.create(nom=nom, categorie=categorie, prix=prix, quantite=quantite)
        
        # Add success message
        # messages.success(request, 'Produit ajouté avec succès.')
        
        # Redirect to product list or dashboard
        return redirect('tableau_de_bord')  # Adjust the redirect URL as needed
    
    # If not POST request, just render the form page
    return render(request, 'tableau_de_bord/form_produit.html')

# def modifier_produit(request):
#     # produit = get_object_or_404(Produit, pk=pk)
    
#     # if request.method == 'POST':
#     #     form = ProduitForm(request.POST, instance=produit)
#     #     if form.is_valid():
#     #         form.save()
#     #         messages.success(request, 'Produit modifié avec succès.')
#     #         return redirect('liste_produits')
#     # else:
#     #     form = ProduitForm(instance=produit)
    
#     # context = {
#     #     'form': form,
#     #     'titre': 'Modifier un produit'
#     # }
    
#     return render(request, 'tableau_de_bord/form_produit.html')

# def supprimer_produit(request, pk):
#     # produit = get_object_or_404(Produit, pk=pk)
    
#     # if request.method == 'POST':
#     #     produit.delete()
#     #     messages.success(request, 'Produit supprimé avec succès.')
#     #     return redirect('liste_produits')
    
#     # context = {
#     #     'produit': produit
#     # }
    
#     return render(request, 'tableau_de_bord/confirmation_suppression.html')

def liste_categories(request):
    # categories = Categorie.objects

    # context = {
    #     'categories': categories
    # }
    
    return render(request, 'tableau_de_bord/categories/liste_categories.html')

def liste_ventes(request):
    # ventes = Commande.objects

    # context = {
    #     'ventes': ventes
    # }
    
    return render(request, 'tableau_de_bord/ventes/liste_ventes.html')

def liste_commandes(request):
    # commandes = Commande.objects

    # context = {
    #     'commandes': commandes
    # }
    
    return render(request, 'tableau_de_bord/commandes/liste_commandes.html')



