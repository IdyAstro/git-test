from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .import views

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
        fields = ['categorie', 'fabricant', 'description','modal']
        



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
    extra=2,
    can_delete=False
)


# forms.py
from django import forms
from .models import Demande

# forms.py
from django import forms
from .models import Demande

from django import forms
from .models import Demande

class DemandeForm(forms.ModelForm):
    class Meta:
        model = Demande
        fields = [
            "prenom", "nom", "email", "direction", "departement",
            "service", "centre", "motif", "materiel", "quantite", "statut"
        ]
        widgets = {
            "prenom": forms.TextInput(attrs={
                "class": "w-full rounded-xl border border-gray-300 p-3 shadow-sm focus:border-teal-500 focus:ring focus:ring-teal-200",
                "placeholder": "Prénom"
            }),
            "nom": forms.TextInput(attrs={
                "class": "w-full rounded-xl border border-gray-300 p-3 shadow-sm focus:border-teal-500 focus:ring focus:ring-teal-200",
                "placeholder": "Nom"
            }),
            "email": forms.EmailInput(attrs={
                "class": "w-full rounded-xl border border-gray-300 p-3 shadow-sm focus:border-teal-500 focus:ring focus:ring-teal-200",
                "placeholder": "Adresse email"
            }),
            "direction": forms.RadioSelect(attrs={
                "class": "space-y-2 text-gray-700"
            }),
            "departement": forms.RadioSelect(attrs={
                "class": "space-y-2 text-gray-700"
            }),
            "service": forms.RadioSelect(attrs={
                "class": "space-y-2 text-gray-700"
            }),
            "centre": forms.RadioSelect(attrs={
                "class": "space-y-2 text-gray-700"
            }),
            "motif": forms.Textarea(attrs={
                "class": "w-full rounded-xl border border-gray-300 p-3 shadow-sm focus:border-teal-500 focus:ring focus:ring-teal-200",
                "rows": 3,
                "placeholder": "Expliquez le motif de votre demande"
            }),
            "materiel": forms.Select(attrs={
                "class": "w-full rounded-xl border border-gray-300 p-3 shadow-sm focus:border-teal-500 focus:ring focus:ring-teal-200"
            }),
            "quantite": forms.NumberInput(attrs={
                "class": "w-full rounded-xl border border-gray-300 p-3 shadow-sm focus:border-teal-500 focus:ring focus:ring-teal-200",
                "placeholder": "Quantité"
            }),
            "statut": forms.Select(attrs={
                "class": "w-full rounded-xl border border-gray-300 p-3 shadow-sm focus:border-teal-500 focus:ring focus:ring-teal-200"
            }),
        }


from django import forms
from .models import Attribution, AttribuMateriel, Materiel

# stock_app/forms.py
from django import forms
from .models import Attribution, AttribuMateriel

# forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Attribution, AttribuMateriel, Approvisionnement, ApproMateriel, Materiel

class AttributionForm(forms.ModelForm):
    class Meta:
        model = Attribution
        fields = [
            'ref','prenom','nom','email','direction','departement','service',
            'locality','etat','utilisateur','demande','approvisionnement'
        ]
        widgets = {
            'direction': forms.RadioSelect(),
            'departement': forms.RadioSelect(),
            'service': forms.RadioSelect(),
            'etat': forms.RadioSelect(),
            'utilisateur': forms.Select(),
            'demande': forms.Select(attrs={"class":"block w-full border rounded p-2"}),
            'approvisionnement': forms.Select(attrs={"class":"block w-full border rounded p-2"}),
        }

class AttribuMaterielForm(forms.ModelForm):
    class Meta:
        model = AttribuMateriel
        fields = ['materiel','quantite']
AttribuMaterielFormSet = inlineformset_factory(
    Attribution,
    AttribuMateriel,
    form=AttribuMaterielForm,
    extra=1,  # on créera les formulaires dynamiquement côté vue
    can_delete=False
)
