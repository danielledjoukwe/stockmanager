from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """Profil utilisateur étendu lié au modèle User de Django"""
    
    ROLE_CHOICES = (
        ('GERANT', 'Gérant'),
        ('MAGASINIER', 'Magasinier'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


class Categorie(models.Model):
    """Modèle de catégorie de produits"""
    
    STATUT_CHOICES = (
        ('ACTIF', 'Actif'),
        ('INACTIF', 'Inactif'),
    )
    
    reference = models.CharField(max_length=10, unique=True)
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='ACTIF')
    
    # Champs d'audit
    createur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='categories_creees')
    date_creation = models.DateTimeField(auto_now_add=True)
    modificateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='categories_modifiees', blank=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nom} ({self.reference})"
    
    def nombre_produits(self):
        """Retourne le nombre de produits dans cette catégorie"""
        return self.produits.count()
    
    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"


class Produit(models.Model):
    """Modèle de produit"""
    
    STATUT_CHOICES = (
        ('EN_STOCK', 'En stock'),
        ('FAIBLE_STOCK', 'Faible stock'),
        ('RUPTURE', 'Rupture'),
    )
    
    reference = models.CharField(max_length=10, unique=True)
    nom = models.CharField(max_length=100)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='produits')
    description = models.TextField(blank=True, null=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantite = models.PositiveIntegerField(default=0)
    seuil_alerte = models.PositiveIntegerField(default=10, help_text="Seuil pour l'alerte de faible stock")
    
    # Champs d'audit
    createur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='produits_crees')
    date_creation = models.DateTimeField(auto_now_add=True)
    modificateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='produits_modifies', blank=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nom} ({self.reference})"
    
    @property
    def statut(self):
        """Détermine automatiquement le statut du produit basé sur la quantité"""
        if self.quantite <= 0:
            return 'RUPTURE'
        elif self.quantite <= self.seuil_alerte:
            return 'FAIBLE_STOCK'
        else:
            return 'EN_STOCK'
        

class ProduitMagasin(models.Model):
    """Modèle de produit"""
    
    STATUT_CHOICES = (
        ('EN_STOCK', 'En stock'),
        ('FAIBLE_STOCK', 'Faible stock'),
        ('RUPTURE', 'Rupture'),
    )
    
    reference = models.CharField(max_length=10, unique=True)
    nom = models.CharField(max_length=100)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='produits')
    description = models.TextField(blank=True, null=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantite = models.PositiveIntegerField(default=0)
    seuil_alerte = models.PositiveIntegerField(default=10, help_text="Seuil pour l'alerte de faible stock")
    
    # Champs d'audit
    createur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='produits_crees')
    date_creation = models.DateTimeField(auto_now_add=True)
    modificateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='produits_modifies', blank=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nom} ({self.reference})"
    
    @property
    def statut(self):
        """Détermine automatiquement le statut du produit basé sur la quantité"""
        if self.quantite <= 0:
            return 'RUPTURE'
        elif self.quantite <= self.seuil_alerte:
            return 'FAIBLE_STOCK'
        else:
            return 'EN_STOCK'
    
    def get_statut_display(self):
        """Retourne le libellé du statut pour l'affichage"""
        statut_dict = dict(self.STATUT_CHOICES)
        return statut_dict.get(self.statut)
    
    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"


class HistoriqueAction(models.Model):
    """Modèle pour enregistrer toutes les actions sur les produits et catégories"""
    
    TYPE_ACTION_CHOICES = (
        ('AJOUT', 'Ajout'),
        ('MODIFICATION', 'Modification'),
        ('SUPPRESSION', 'Suppression'),
    )
    
    TYPE_OBJET_CHOICES = (
        ('PRODUIT', 'Produit'),
        ('CATEGORIE', 'Catégorie'),
    )
    
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actions')
    type_action = models.CharField(max_length=15, choices=TYPE_ACTION_CHOICES)
    type_objet = models.CharField(max_length=15, choices=TYPE_OBJET_CHOICES)
    identifiant_objet = models.CharField(max_length=10, help_text="Référence du produit ou de la catégorie")
    nom_objet = models.CharField(max_length=100, help_text="Nom du produit ou de la catégorie")
    details = models.TextField(blank=True, null=True, help_text="Détails supplémentaires de l'action")
    date_action = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_type_action_display()} de {self.get_type_objet_display()} '{self.nom_objet}' par {self.utilisateur.username}"
    
    class Meta:
        verbose_name = "Historique d'action"
        verbose_name_plural = "Historique des actions"
        ordering = ['-date_action']