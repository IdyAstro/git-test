from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ApproMateriel, AttribuMateriel, Stock
@receiver(post_save, sender=ApproMateriel)
def update_stock_on_appro(sender, instance, created, **kwargs):
    """Mise à jour du stock après un approvisionnement"""
    stock, _ = Stock.objects.get_or_create(materiel=instance.materiel)
    if created:
        stock.quantite += instance.quantite
    else:
        # Si on modifie la quantité d'un appro déjà existant
        stock.quantite = sum(a.quantite for a in ApproMateriel.objects.filter(materiel=instance.materiel))
        stock.quantite -= sum(attr.quantite for attr in AttribuMateriel.objects.filter(materiel=instance.materiel))
    stock.save()


@receiver(post_save, sender=AttribuMateriel)
def update_stock_on_attri(sender, instance, created, **kwargs):
    """Mise à jour du stock après une attribution"""
    stock, _ = Stock.objects.get_or_create(materiel=instance.materiel)
    if created:
        stock.quantite -= instance.quantite
    else:
        # Recalcule le stock si on modifie l'attribution
        stock.quantite = sum(a.quantite for a in ApproMateriel.objects.filter(materiel=instance.materiel))
        stock.quantite -= sum(attr.quantite for attr in AttribuMateriel.objects.filter(materiel=instance.materiel))
    stock.save()


@receiver(post_delete, sender=ApproMateriel)
@receiver(post_delete, sender=AttribuMateriel)
def recalc_stock_on_delete(sender, instance, **kwargs):
    """Recalcule le stock si un mouvement est supprimé"""
    stock, _ = Stock.objects.get_or_create(materiel=instance.materiel)
    stock.quantite = sum(a.quantite for a in ApproMateriel.objects.filter(materiel=instance.materiel))
    stock.quantite -= sum(attr.quantite for attr in AttribuMateriel.objects.filter(materiel=instance.materiel))
    stock.save()



