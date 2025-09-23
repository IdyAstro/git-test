from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label = 'Password',
        strip= False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "new-password",
            "class": "input w-full",
            "placeholder": "Confirmez votre  passe"

            
        
        }), help_text=None),
    password2 = forms.CharField(
        label="Confirmation du mot de passe",
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "new-password",
            "class": "input w-full",
            "placeholder": "Confirmez votre  passe"
        }),
        help_text=None  # Enlève aussi
    )
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("password1","password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Supprimer le help_text de tous les champs
        for fieldname in self.fields:
            self.fields[fieldname].help_text = None



from django import forms
from .models import Materiel

class MaterielForm(forms.ModelForm):
    class Meta:
        model = Materiel
        fields = ['categorie', 'fabricant', 'description','modal','serie']
        



# forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Approvisionnement, ApproMateriel

class ApprovisionnementForm(forms.ModelForm):
    class Meta:
        model = Approvisionnement
        fields = ['utilisateur']

ApproMaterielFormSet = inlineformset_factory(
    Approvisionnement,
    ApproMateriel,
    fields=['materiel', 'quantite'],
    extra=3,
    
    can_delete=False
)


# forms.py
from django import forms
from .models import Demande

# forms.py
from django import forms
from .models import Demande

class DemandeForm(forms.ModelForm):
    class Meta:
        model = Demande
        fields = [
            "prenom", "nom", "email", "direction", "departement",
            "service", "centre","motif", "materiel", "quantite", "statut"
        ]
        widgets = {
            "prenom": forms.TextInput(attrs={"class": "border rounded w-full p-2"}),
            "nom": forms.TextInput(attrs={"class": "border rounded w-full p-2"}),
            "email": forms.EmailInput(attrs={"class": "border rounded w-full p-2"}),
            "direction": forms.TextInput(attrs={"class": "border rounded w-full p-2"}),
            "departement": forms.TextInput(attrs={"class": "border rounded w-full p-2"}),
            "service": forms.TextInput(attrs={"class": "border rounded w-full p-2"}),
            "centre": forms.TextInput(attrs={"class": "border rounded w-full p-2"}),
            "motif": forms.TextInput(attrs={"class": "border rounded w-full p-2"}),
            "materiel": forms.Select(attrs={"class": "border rounded w-full p-2"}),
            "quantite": forms.NumberInput(attrs={"class": "border rounded w-full p-2"}),
            "statut": forms.Select(attrs={"class": "border rounded w-full p-2"}),
        }



from django import forms
from .models import Attribution, AttribuMateriel, Materiel

class AttributionForm(forms.ModelForm):
    class Meta:
        model = Attribution
        fields = ["utilisateur","ref","usager"]
        widgets = {
            "ref":forms.TextInput(attrs={
                'class':'border rounded my-3 p-2',
                'placeholder':'Ex : BKO-S-V-SPI-OO1'
            }),
            "usager":forms.TextInput(attrs={
                'class':'border rounded my-3 p-2'
            })


        }



class AttribuMaterielForm(forms.ModelForm):
    class Meta:
        model = AttribuMateriel
        fields = ["materiel", "quantite"]
        widgets = {
            "materiel": forms.Select(attrs={"class": "border p-2 rounded w-full"}),
            "quantite": forms.NumberInput(attrs={"class": "border p-2 rounded w-full", "min": 1}),
        }
        