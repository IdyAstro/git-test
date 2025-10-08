from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField # pyright: ignore[reportMissingImports]

class Utilisateur(models.Model):
    nom = models.CharField(max_length=40)

    def __str__(self):
        return self.nom


class Categorie(models.Model):
    label = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.label


class Materiel(models.Model):
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    fabricant = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    modal = models.CharField(max_length=100, default="modèle")
    
    def __str__(self):
        return f"{self.categorie} - {self.fabricant} - {self.modal}"

from django.db import models

class Direction(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom


class Departement(models.Model):
    nom = models.CharField(max_length=100)
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, related_name="departements")

    def __str__(self):
        return f"{self.nom} ({self.direction.nom})"


class Service(models.Model):
    nom = models.CharField(max_length=100)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE, related_name="services")

    def __str__(self):
        return f"{self.nom} ({self.departement.nom})"

class Demande(models.Model):


    prenom = models.CharField(max_length=40)
    nom = models.CharField(max_length=40)
    email = models.EmailField(max_length=50)

    direction = models.ForeignKey(Direction, on_delete=models.CASCADE)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
   

    tel = PhoneNumberField(null=True, blank=True, unique=True)



    motif = models.TextField(max_length=255)
    materiel = models.ForeignKey("Materiel", on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    statut = models.CharField(
        max_length=20,
        choices=[
            ("en_attente", "En attente"),
            ("acceptee", "Acceptée"),
            ("refusee", "Refusée"),
        ],
        default="en_attente",
    )
    date_demande = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Demande de {self.materiel.fabricant} par {self.prenom} {self.nom}"


class Approvisionnement(models.Model):
    date_appro = models.DateTimeField(auto_now_add=True)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Approvisionnement du {self.date_appro.strftime('%Y-%m-%d %H:%M')}"


class ApproMateriel(models.Model):
    materiel = models.ForeignKey(Materiel, on_delete=models.CASCADE)
    appro = models.ForeignKey(Approvisionnement, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantite} x {self.materiel}"


class Attribution(models.Model):
    date_attri = models.DateTimeField(auto_now_add=True)
    ref = models.CharField(max_length=20, null=True, blank=True)
    prenom = models.CharField(max_length=40, null=True, blank=True)
    nom = models.CharField(max_length=40, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)

    # === Remplacer les CharFields par des ForeignKey ===
    direction = models.ForeignKey(Direction, on_delete=models.SET_NULL, null=True, blank=True)
    departement = models.ForeignKey(Departement, on_delete=models.SET_NULL, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)

    locality = models.CharField(max_length=20, null=True, blank=True)
    serie = models.CharField(max_length=50, null=True, blank=True)
    etat = models.CharField(
        max_length=20,
        choices=[
            ("bon", "BON"),
            ("pass", "PASSABLE"),
            ("endo", "ENDOMMAGER"),
        ],
        default="bon",
    )

    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True)
    demande = models.ForeignKey(
        Demande, on_delete=models.SET_NULL, null=True, blank=True,
        help_text="Demande à l’origine de cette attribution"
    )
    approvisionnement = models.ForeignKey(
        Approvisionnement, on_delete=models.SET_NULL, null=True, blank=True,
        help_text="Approvisionnement dont provient le matériel"
    )

    def __str__(self):
        return f"Attribution du {self.date_attri.strftime('%Y-%m-%d %H:%M')}"



class AttribuMateriel(models.Model):
    materiel = models.ForeignKey(Materiel, on_delete=models.CASCADE)
    attri = models.ForeignKey(Attribution, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()

    def clean(self):
        """Empêche d’attribuer plus que le stock disponible"""
        stock, _ = Stock.objects.get_or_create(materiel=self.materiel)
        if self.pk:
            ancienne_qte = AttribuMateriel.objects.get(pk=self.pk).quantite
        else:
            ancienne_qte = 0

        nouvelle_qte = self.quantite - ancienne_qte
        if nouvelle_qte > stock.quantite:
            raise ValidationError(
                f"Stock insuffisant ! Disponible : {stock.quantite}, demandé : {nouvelle_qte}"
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantite} x {self.materiel}"


class Stock(models.Model):
    materiel = models.ForeignKey(Materiel, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.materiel} : {self.quantite} en stock"


# === SIGNALS ===
@receiver(post_save, sender=ApproMateriel)
def update_stock_on_appro(sender, instance, created, **kwargs):
    stock, _ = Stock.objects.get_or_create(materiel=instance.materiel)
    if created:
        stock.quantite += instance.quantite
    else:
        ancienne = ApproMateriel.objects.get(pk=instance.pk).quantite
        stock.quantite += instance.quantite - ancienne
    stock.save()


@receiver(post_delete, sender=ApproMateriel)
def update_stock_on_delete_appro(sender, instance, **kwargs):
    stock, _ = Stock.objects.get_or_create(materiel=instance.materiel)
    stock.quantite -= instance.quantite
    stock.save()


@receiver(post_save, sender=AttribuMateriel)
def update_stock_on_attri(sender, instance, created, **kwargs):
    stock, _ = Stock.objects.get_or_create(materiel=instance.materiel)
    if created:
        stock.quantite -= instance.quantite
    else:
        ancienne = AttribuMateriel.objects.get(pk=instance.pk).quantite
        stock.quantite -= instance.quantite - ancienne
    stock.save()


@receiver(post_delete, sender=AttribuMateriel)
def update_stock_on_delete_attri(sender, instance, **kwargs):
    stock, _ = Stock.objects.get_or_create(materiel=instance.materiel)
    stock.quantite += instance.quantite
    stock.save()
