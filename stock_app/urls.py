from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('',views.connexion,name="connexion"),
    path('inscription/',views.inscription,name="inscription"),
    path('home/',views.home,name="home"),

    #=====================CATEGORIES==========================================
    path('categories/', views.liste_categories, name='liste_categories'),
    path('categories/ajouter/', views.ajouter_categorie, name='ajouter_categorie'),
    path('categories/modifier/<int:id>/', views.modifier_categorie, name='modifier_categorie'),
    path('categories/supprimer/<int:id>/', views.supprimer_categorie, name='supprimer_categorie'),
    #======================MATERIEL=================================================



    path("materiels/", views.materiel_list, name="materiel_list"),
    path("materiels/add/", views.materiel_create, name="materiel_create"),
    path("materiels/<int:pk>/edit/", views.materiel_update, name="materiel_update"),
    path("materiels/<int:pk>/delete/", views.materiel_delete, name="materiel_delete"),
    
    path("appros/", views.liste_appros, name="liste_appros"),
    path("appros/nouveau/", views.creer_appro, name="creer_appro"),
    
    #=======================DEMANDE==============================

    path("demandes/", views.liste_demandes, name="liste_demandes"),
    path("demandes/nouvelle/", views.creer_demande, name="creer_demande"),
    path("demandes/<int:pk>/", views.detail_demande, name="detail_demande"),
    path("demandes/<int:pk>/modifier/", views.modifier_demande, name="modifier_demande"),
    path("demandes/<int:pk>/supprimer/", views.supprimer_demande, name="supprimer_demande"),
    path("demandes/export/", views.export_demandes, name="export_demandes"),

    path("attributions/nouveau/", views.nouvelle_attribution, name="nouvelle_attribution"),
    path("attributions/", views.liste_attributions, name="liste_attributions"), 
    path("dashboard/", views.dashboard, name="dashboard"),
    path("deconnexion/",views.deconnexion,name="deconnexion"), 



    
]