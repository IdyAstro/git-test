from django.shortcuts import render , get_object_or_404, redirect
from .models import *
from .forms import *
# Create your views here.
from django.contrib.auth.decorators import login_required
from .models import *
import csv
from django.http import HttpResponse

from django.db.models import Sum
from datetime import  timedelta
from datetime import datetime
from django.core.paginator import Paginator
from .models import Materiel
from .forms import MaterielForm ,ApproMaterielFormSet,ApprovisionnementForm,DemandeForm
from django.contrib.auth import login , authenticate , logout
from django.contrib import messages 

# Create your views here.
def inscription(reqest):
      if reqest.method == "POST":
        forms = CustomUserCreationForm(reqest.POST)
        if forms.is_valid():
           forms.save()
           return redirect('connexion')
      else:
        forms = CustomUserCreationForm()
      return render(reqest,'inscription.html',{'forms':forms})



def connexion(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect ❌")

    # Ici, GET ou POST échoué → juste afficher le template
    return render(request, "login.html")
from django.contrib.auth import logout
from django.shortcuts import redirect

def deconnexion(request):
    logout(request)
    return redirect("connexion")  # Redirige vers la page de connexion après déconnexion



@login_required
def home(request):
    # Stats simples
   #stockTotal = int(Stock.objects.aaggregate(sum('quantite')))

    # Evolution 7 derniers jours
    
   return render(request, "home.html")


from django.shortcuts import render, redirect, get_object_or_404
from .models import Categorie
from django.contrib import messages
#=========================CATEGORIE================================================================
# ---- Liste ----
@login_required
def liste_categories(request):
    categories = Categorie.objects.all().order_by('id')
    return render(request, 'categories/liste.html', {'categories': categories})

# ---- Ajouter ----
@login_required
def ajouter_categorie(request):
    if request.method == 'POST':
        label = request.POST.get('label')
        if Categorie.objects.filter(label__iexact=label).exists():
            messages.error(request, "Cette catégorie existe déjà.")
        else:
            Categorie.objects.create(label=label)
            messages.success(request, "Catégorie ajoutée avec succès.")
            return redirect('liste_categories')
    return render(request, 'categories/form.html')

# ---- Modifier ----
@login_required
def modifier_categorie(request, id):
    categorie = get_object_or_404(Categorie, id=id)
    if request.method == 'POST':
        label = request.POST.get('label')
        if label:
            categorie.label = label
            categorie.save()
            messages.success(request, "Catégorie modifiée avec succès !")
            return redirect('liste_categories')
    return render(request, 'categories/form.html', {'categorie': categorie})

# ---- Supprimer ----
@login_required
def supprimer_categorie(request, id):
    categorie = get_object_or_404(Categorie, id=id)
    categorie.delete()
    messages.success(request, "Catégorie supprimée !")
    return redirect('liste_categories')
#=============================MATERIEL=============================================================





# ---- LISTE avec filtres et pagination ----
@login_required
def materiel_list(request):
    query = request.GET.get("q")
    categorie = request.GET.get("categorie")

    materiels = Materiel.objects.all()

    if query:
        materiels = materiels.filter(fabricant__icontains=query) | materiels.filter(description__icontains=query) | materiels.filter(modal__icontains=query) 

    if categorie:
        materiels = materiels.filter(categorie__id=categorie)

    paginator = Paginator(materiels, 5)  # 5 matériels par page
    page = request.GET.get("page")
    materiels_page = paginator.get_page(page)

    return render(request, "materiel/liste.html", {"materiels": materiels_page})

# ---- CREATE ----
@login_required
def materiel_create(request):
    if request.method == "POST":
        form = MaterielForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("materiel_list")
    else:
        form = MaterielForm()
    return render(request, "materiel/form.html", {"form": form})

# ---- UPDATE ----
@login_required
def materiel_update(request, pk):
    materiel = get_object_or_404(Materiel, pk=pk)
    if request.method == "POST":
        form = MaterielForm(request.POST, instance=materiel)
        if form.is_valid():
            form.save()
            return redirect("materiel_list")
    else:
        form = MaterielForm(instance=materiel)
    return render(request, "materiel/modif.html", {"form": form})

# ---- DELETE ----
@login_required
def materiel_delete(request, pk):
    materiel = get_object_or_404(Materiel, pk=pk)
    if request.method == "POST":
        materiel.delete()
        return redirect("materiel_list")
    return render(request, "materiel/confirme_suppression.html", {"materiel": materiel})



# views.py


#====================================APPROVISIONNEMENT=======================================================================
@login_required
def liste_appros(request):
    
    appros = Approvisionnement.objects.all().order_by('-date_appro')
    paginator = Paginator(appros, 2)
    page = request.GET.get("page")
    appros_page = paginator.get_page(page)
    return render(request, "appro/liste.html", {"appros": appros_page})
@login_required
def creer_appro(request):
    if request.method == "POST":
        appro_form = ApprovisionnementForm(request.POST)
        formset = ApproMaterielFormSet(request.POST)

        if appro_form.is_valid() and formset.is_valid():
            appro = appro_form.save()
            formset.instance = appro
            formset.save()
            return redirect("liste_appros")
    else:
        appro_form = ApprovisionnementForm()
        formset = ApproMaterielFormSet()

    return render(request, "appro/form.html", {
        "appro_form": appro_form,
        "formset": formset
    })


#===================================================DEMANDE==========================================================
# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Demande
from .forms import DemandeForm

# ---- CREATE ----
@login_required
def creer_demande(request):
    if request.method == "POST":
        form = DemandeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("liste_demandes")
    else:
        form = DemandeForm()
    return render(request, "demandes/creer.html", {"form": form})

# ---- READ (Liste) ----
@login_required


@login_required
def export_demandes(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="demandes.csv"'

    writer = csv.writer(response)
    writer.writerow(['Prénom', 'Nom', 'Matériel', 'Quantité', 'Statut', 'Date'])

    for d in Demande.objects.all().order_by("-date_demande"):
        writer.writerow([d.prenom, d.nom, d.materiel, d.quantite, d.get_statut_display(), d.date_demande])

    return response

def liste_demandes(request):
    query = request.GET.get("q")
    demandes = Demande.objects.all().order_by("-date_demande")
    if query:
        demandes = demandes.filter(prenom__icontains=query) | demandes.filter(nom__icontains=query)
    paginator = Paginator(demandes, 3)  
    page = request.GET.get("page")
    demandes_page = paginator.get_page(page)
    return render(request, "demandes/liste.html", {"demandes": demandes_page})

# ---- READ (Détail) ----
@login_required
def detail_demande(request, pk):
    demande = get_object_or_404(Demande, pk=pk)
    return render(request, "demandes/detail.html", {"demande": demande})

# ---- UPDATE ----
@login_required
def modifier_demande(request, pk):
    demande = get_object_or_404(Demande, pk=pk)
    if request.method == "POST":
        form = DemandeForm(request.POST, instance=demande)
        if form.is_valid():
            form.save()
            return redirect("liste_demandes")
    else:
        form = DemandeForm(instance=demande)
    return render(request, "demandes/modifier.html", {"form": form})

# ---- DELETE ----
@login_required
def supprimer_demande(request, pk):
    demande = get_object_or_404(Demande, pk=pk)
    if request.method == "POST":
        demande.delete()
        return redirect("liste_demandes")
    return render(request, "demandes/supprimer.html", {"demande": demande})



    
from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from django.contrib import messages
from .models import Attribution, AttribuMateriel
from .forms import AttributionForm, AttribuMaterielForm

@login_required
def liste_attributions(request):
    attributions = Attribution.objects.all().order_by("-date_attri")
    return render(request, "attributions/liste.html", {
        "attributions": attributions,
    })
@login_required
def nouvelle_attribution(request):
    AttribuFormSet = modelformset_factory(AttribuMateriel, form=AttribuMaterielForm, extra=1, can_delete=True)

    if request.method == "POST":
        attribution_form = AttributionForm(request.POST)
        formset = AttribuFormSet(request.POST, queryset=AttribuMateriel.objects.none())

        if attribution_form.is_valid() and formset.is_valid():
            attribution = attribution_form.save()

            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get("DELETE", False):
                    attribu_materiel = form.save(commit=False)
                    attribu_materiel.attri = attribution
                    try:
                        attribu_materiel.save()
                    except ValueError as e:
                        messages.error(request, str(e))
                        attribution.delete()
                        return redirect("nouvelle_attribution")

            messages.success(request, "✅ Attribution enregistrée avec succès.")
            return redirect("liste_attributions")

    else:
        attribution_form = AttributionForm()
        formset = AttribuFormSet(queryset=AttribuMateriel.objects.none())

    return render(request, "attributions/form.html", {
        "attribution_form": attribution_form,
        "formset": formset,
    })



import json
from django.shortcuts import render
from django.db.models import Sum, Count
from .models import Stock, Demande, ApproMateriel, AttribuMateriel, Materiel
@login_required
def dashboard(request):
    total_stock = Stock.objects.aggregate(total=Sum("quantite"))["total"] or 0
    total_materiels = Materiel.objects.count()
    total_appros = ApproMateriel.objects.aggregate(total=Sum("quantite"))["total"] or 0
    total_attris = AttribuMateriel.objects.aggregate(total=Sum("quantite"))["total"] or 0

    demandes_stats = Demande.objects.values("statut").annotate(nb=Count("id"))

    top_appros = (
        ApproMateriel.objects.values("materiel__description")
        .annotate(total=Sum("quantite"))
        .order_by("-total")[:5]
    )
    top_attris = (
        AttribuMateriel.objects.values("materiel__description")
        .annotate(total=Sum("quantite"))
        .order_by("-total")[:5]
    )

    stock_par_categorie = (
        Stock.objects.values("materiel__categorie__label")
        .annotate(total=Sum("quantite"))
    )

    stock_critique = Stock.objects.filter(quantite__lt=5)

    # --- Préparer les listes JSON pour Chart.js ---
    chart_stock_labels = [s["materiel__categorie__label"] for s in stock_par_categorie]
    chart_stock_data = [s["total"] for s in stock_par_categorie]

    chart_demande_labels = [d["statut"] for d in demandes_stats]
    chart_demande_data = [d["nb"] for d in demandes_stats]

    context = {
        "total_stock": total_stock,
        "total_materiels": total_materiels,
        "total_appros": total_appros,
        "total_attris": total_attris,
        "top_appros": list(top_appros),
        "top_attris": list(top_attris),
        "stock_critique": stock_critique,

        # JSON safe
        "chart_stock_labels": json.dumps(chart_stock_labels),
        "chart_stock_data": json.dumps(chart_stock_data),
        "chart_demande_labels": json.dumps(chart_demande_labels),
        "chart_demande_data": json.dumps(chart_demande_data),
    }
    return render(request, "dashboard.html", context)
