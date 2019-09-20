from datetime import timedelta

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site

from entitaet.models import Person
from .models import Dienst, Teilnahme


signer_umfragen = TimestampSigner(salt="DienstUmfrage")
signer_info = TimestampSigner(salt="DienstInfo")


def umfrage_antwort(request, token, antwort):
    try:
        person_id, dienst_id = \
            signer_umfragen.unsign(token, max_age=timedelta(days=30)).split(":")
        person = Person.objects.get(pk=person_id)
        dienst = Dienst.objects.get(pk=dienst_id)
    except (Person.DoesNotExist, BadSignature):
        return HttpResponse("Authorization failed", status=403)
    except SignatureExpired:
        return HttpResponse("Signature expired", status=401)
    else:
        teilnahme, _ = Teilnahme.objects.get_or_create(person=person, dienst=dienst)
        teilnahme.vorab = antwort
        teilnahme.save()

        token = signer_info.sign(dienst.id)

        return redirect(reverse("dienst_info", kwargs={"token": token}))


def dienst_info(request, token):
    try:
        dienst_id = signer_info.unsign(token, max_age=timedelta(minutes=20))
        dienst = Dienst.objects.get(pk=dienst_id)
    except (Person.DoesNotExist, BadSignature):
        return HttpResponse("Authorization failed", status=403)
    except SignatureExpired:
        return HttpResponse("Signature expired", status=401)
    else:
        mitglieder = dienst.gruppe.entitaeten.filter(person__isnull=False).select_subclasses("person")
        teilnahmen = []
        for mitglied in mitglieder:
            try:
                teilnahme = Teilnahme.objects.get(person=mitglied, dienst=dienst).vorab
            except Teilnahme.DoesNotExist:
                teilnahme = Teilnahme._meta.get_field("vorab").default
            teilnahmen.append({"person": mitglied, "teilnahme": teilnahme})

        return render(request, "dienst/info.html", {"dienst": dienst, "teilnahmen": teilnahmen})


def get_token(request):
    token = signer_umfragen.sign("1:1")
    domain = get_current_site(request).domain
    path_an = reverse("umfrage_antwort", kwargs={"token": token, "antwort": Teilnahme.ANWESEND})
    link_an = "{}://{}{}".format(request.scheme, domain, path_an)
    path_ab = reverse("umfrage_antwort", kwargs={"token": token, "antwort": Teilnahme.ABWESEND})
    link_ab = "{}://{}{}".format(request.scheme, domain, path_ab)
    path_unklar = reverse("umfrage_antwort", kwargs={"token": token, "antwort": Teilnahme.UNKLAR})
    link_unklar = "{}://{}{}".format(request.scheme, domain, path_unklar)

    links = ["<a href=\"{}\">{}</a>".format(link, label) for label, link in {"an": link_an, "ab": link_ab, "unklar": link_unklar}.items()]
    return HttpResponse(links)
