from django.contrib import admin # pyright: ignore[reportMissingModuleSource]
from django.urls import path # pyright: ignore[reportMissingModuleSource]
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
    path('appro/<int:pk>/', views.detail_appro, name='detail_appro'),
    path('appro/<int:pk>/modifier/', views.modifier_appro, name='modifier_appro'),
    path("appro-his/", views.historique_appros, name="historique_appros"),

    
    #=======================DEMANDE==============================

    path("demandes/", views.liste_demandes, name="liste_demandes"),
    path("demandes/nouvelle/", views.creer_demande, name="creer_demande"),
    path("demandes/<int:pk>/", views.detail_demande, name="detail_demande"),
    path("demandes/<int:pk>/modifier/", views.modifier_demande, name="modifier_demande"),
    path("demandes/<int:pk>/supprimer/", views.supprimer_demande, name="supprimer_demande"),
    path("demandes/export/", views.export_demandes_xls, name="export_demandes_xls"),
    path("demandes/exhaussive/", views.listes_exhaussive, name="listes_exhaussive"),

    path("attributions/nouveau/", views.nouvelle_attribution, name="nouvelle_attribution"),
    path("attributions/", views.liste_attributions, name="liste_attributions"),
     
    path("dashboard/", views.dashboard, name="dashboard"),
    path("deconnexion/",views.deconnexion,name="deconnexion"),
    path("new/",views.nouvel_approvisionnement,name="nouvel_approvisionnement"), 
    path("attributions/export/", views.exportation_csv, name="exportation_csv"),
    path("attributions/<int:pk>/", views.attribution_detail, name="attribution_detail"),
    path('attributions/<int:pk>/edit/', views.edit_attribution, name='edit_attribution'),
    path('attributions/<int:pk>/delete/', views.delete_attribution, name='delete_attribution'),
     path('export_attributions/', views.export_attributions, name='export_attributions'),
    path("export-rapport/", views.export_rapport_excel, name="export_rapport"),
    path("rapport-global/", views.rapport_global, name="rapport_global"),
    path("rapport-direction/", views.rapport_par_direction, name="rapport_par_direction"),
    path("rapport-attribution/", views.rapport_attributions, name="rapport_attributions"),
    path("rapport/", views.rapport_attributions, name="rapport_attributions"),
    path("rapport-appro/", views.rapport_approvisionnement, name="rapport_approvisionnement"),
    path("rapport-appro/", views.rapport_approvisionnement, name="rapport_approvisionnement"),
    path("ajax/materiels/<int:appro_id>/", views.get_materiels_by_appro, name="get_materiels_by_appro"),
    path('ajax/load-departements/', views.load_departements, name='ajax_load_departements'),
    path('ajax/load-services/', views.load_services, name='ajax_load_services'),
]