from django.contrib import admin # pyright: ignore[reportMissingModuleSource]
from .models import *
# Register your models here.
admin.site.register(Categorie)
admin.site.register(Materiel)
admin.site.register(ApproMateriel)
admin.site.register(Approvisionnement)
admin.site.register(Demande)
admin.site.register(Attribution)
admin.site.register(AttribuMateriel)
admin.site.register(Stock)

