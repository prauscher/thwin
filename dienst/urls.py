from django.urls import path

from . import views

urlpatterns = [
    path('umfrage/<str:token>/<str:antwort>', views.umfrage_antwort, name="umfrage_antwort"),
    path('info/<str:token>', views.dienst_info, name="dienst_info"),
    path('tmp', views.get_token),
]
