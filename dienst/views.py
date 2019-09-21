from datetime import timedelta

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site

from entitaet.models import Person
from entitaet.login import save_login, require_login, check_permission
from .models import Dienst, Teilnahme


signer_umfragen = TimestampSigner(salt="DienstUmfrage")


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
        save_login(request, person)

        teilnahme, _ = Teilnahme.objects.get_or_create(person=person, dienst=dienst)
        teilnahme.vorab = antwort
        teilnahme.save()

        return redirect(reverse("dienst_info", kwargs={"dienst_id": dienst.id}))


@require_login
def umfrage_versenden(request, dienst_id):
    try:
        dienst = Dienst.objects.get(pk=dienst_id)
        check_permission(request, dienst.gruppe, 3)
    except Dienst.DoesNotExist:
        pass
    except ValueError:
        return HttpResponse("Forbidden", status=403)
    else:
        mitglieder = dienst.gruppe.get_mitglieder()
        for person in mitglieder:
            token = signer_umfragen.sign("{}:{}".format(person.id, dienst.id))
            domain = get_current_site(request).domain
            moeglichkeiten = Teilnahme.OPTIONS

            for mc, ml in moeglichkeiten:
                path = reverse("umfrage_antwort", kwargs={"token": token, "antwort": mc})
                link = "{}://{}{}".format(request.scheme, domain, path)
                print(person, ml, link)

        return HttpResponse("Versendet")


@require_login
def anwesenheit_setzen(request, dienst_id, person_id, vorab, ist):
    try:
        dienst = Dienst.objects.get(pk=dienst_id)
        person = Person.objects.get(pk=person_id)
        check_permission(request, dienst.gruppe, 4)
    except (Person.DoesNotExist, Dienst.DoesNotExist):
        pass
    except ValueError:
        return HttpResponse("Forbidden", status=403)
    else:
        teilnahme, _ = Teilnahme.objects.get_or_create(person=person, dienst=dienst)
        teilnahme.vorab = vorab
        teilnahme.ist = ist
        teilnahme.save()

        return redirect(reverse("dienst_info", kwargs={"dienst_id": dienst.id}))


@require_login
def dienst_info(request, dienst_id):
    try:
        dienst = Dienst.objects.get(pk=dienst_id)
        check_permission(request, dienst.gruppe, 3)
    except Dienst.DoesNotExist:
        pass
    except ValueError:
        return HttpResponse("Forbidden", status=403)
    else:
        mitglieder = dienst.gruppe.get_mitglieder()
        teilnahmen = []
        for mitglied in mitglieder:
            try:
                teilnahme = Teilnahme.objects.get(person=mitglied, dienst=dienst)
            except Teilnahme.DoesNotExist:
                teilnahme = Teilnahme(person=mitglied, dienst=dienst)
            teilnahmen.append({"person": mitglied, "teilnahme": teilnahme})

        return render(request, "dienst/info.html", {"dienst": dienst, "teilnahmen": teilnahmen, "optionen": Teilnahme.OPTIONS})


def get_token(request):
    token = signer_umfragen.sign("1:1")
    domain = get_current_site(request).domain
    path_an = reverse("umfrage_antwort", kwargs={"token": token, "antwort": Teilnahme.ANWESEND})
    link_an = "{}://{}{}".format(request.scheme, domain, path_an)
    path_ab = reverse("umfrage_antwort", kwargs={"token": token, "antwort": Teilnahme.ABWESEND})
    link_ab = "{}://{}{}".format(request.scheme, domain, path_ab)
    path_unklar = reverse("umfrage_antwort", kwargs={"token": token, "antwort": Teilnahme.UNKLAR})
    link_unklar = "{}://{}{}".format(request.scheme, domain, path_unklar)

    links = " - ".join(["<a href=\"{}\">{}</a>".format(link, label) for label, link in {"an": link_an, "ab": link_ab, "unklar": link_unklar}.items()])
    return HttpResponse(links)
