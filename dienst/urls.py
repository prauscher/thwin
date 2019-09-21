from django.urls import path

from . import views

urlpatterns = [
    path('umfrage/<str:token>/<str:antwort>', views.umfrage_antwort, name="umfrage_antwort"),
    path('<int:dienst_id>/anwesenheit/<int:person_id>/<str:vorab>-<str:ist>', views.anwesenheit_setzen, name="anwesenheit_setzen"),
    path('<int:dienst_id>/info', views.dienst_info, name="dienst_info"),
    path('<int:dienst_id>/umfrage', views.umfrage_versenden, name="umfrage_versenden"),
    path('tmp', views.get_token),
]
