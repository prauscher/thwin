from datetime import timedelta, datetime
from collections import defaultdict

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
import pyotp

from .models import Person, Rollenzugehoerigkeit


signer = TimestampSigner(salt="PersonLogin")


def require_login(func):
    def _wrapper(request, *args, **kwargs):
        if "person_id" not in request.session:
            return redirect(reverse("login"))

        return func(request, *args, **kwargs)
    return _wrapper


def check_permission(request, gruppe, berechtigung_id):
    letzter_check = datetime.fromtimestamp(request.session["berechtigungen_check"])
    if datetime.now() - letzter_check > timedelta(hours=1):
        person = Person.objects.get(id=request.session["person_id"])
        request.session["berechtigungen"] = _calculate_permissions(person)
        request.session["berechtigungen_check"] = datetime.now().timestamp()

    if str(gruppe.id) in request.session["berechtigungen"] and [berechtigung_id, False] in request.session["berechtigungen"][str(gruppe.id)]:
        return True

    current_gruppe = gruppe
    # Schutz vor Endlosschleifen
    visited_gruppen = []
    while True:
        if str(current_gruppe.id) in request.session["berechtigungen"] and [berechtigung_id, True] in request.session["berechtigungen"][str(current_gruppe.id)]:
            return True

        visited_gruppen.append(current_gruppe)
        current_gruppe = current_gruppe.uebergeordnet

        if current_gruppe is None or current_gruppe in visited_gruppen:
            break

    raise ValueError


def _calculate_permissions(person):
    berechtigungen = defaultdict(lambda: list())

    rollenzugehoerigkeiten = Rollenzugehoerigkeit.objects.filter(entitaet=person)
    for rollenzugehoerigkeit in rollenzugehoerigkeiten:
        gruppe = rollenzugehoerigkeit.gruppe
        rolle = rollenzugehoerigkeit.rolle
        rollenberechtigungen = [[freigabe.berechtigung.id, freigabe.untergruppen] for freigabe in rolle.freigaben.all()]

        berechtigungen[str(gruppe.id)].extend(rollenberechtigungen)

    return berechtigungen


def save_login(request, person):
    request.session["person_id"] = person.id
    request.session["berechtigungen"] = _calculate_permissions(person)
    request.session["berechtigungen_check"] = datetime.now().timestamp()


def login_by_code(request):
    try:
        person = Person.objects.get(mail=request.POST["mail"])
        if not person.auth_code:
            raise ValueError

        otp = pyotp.TOTP(person.auth_code)
        if not otp.verify(request.POST["token"]):
            raise ValueError

        save_login(request, person)
        return redirect(reverse("index"))
    except KeyError:
        return render(request, "login/login_form.html")
    except (Person.DoesNotExist, ValueError):
        return render(request, "login/login_form.html", {"error": "Auth failed"})


def login_by_token(request, token):
    try:
        mail = signer.unsign(token, max_age=timedelta(days=3))
        person = Person.objects.get(mail=mail)
    except (Person.DoesNotExist, BadSignature):
        return HttpResponse("Authorization failed", status=403)
    except SignatureExpired:
        return HttpResponse("Signature expired", status=401)
    else:
        save_login(request, person)
        return redirect(reverse("index"))


def logout(request):
    try:
        del request.session["person_id"]
        del request.session["berechtigungen"]
        del request.session["berechtigungen_check"]
    except KeyError:
        pass

    return redirect(reverse("index"))


def request_token(request):
    try:
        user = Person.objects.get(mail=request.POST["mail"])
    except KeyError:
        return render(request, "login/request_link_form.html")
    except Person.DoesNotExist:
        # fail silently to prevent information leakage
        pass
    else:
        token = signer.sign(user.mail)

        domain = get_current_site(request).domain
        path = reverse("login_by_token", kwargs={"token": token})
        link = "{}://{}{}".format(request.scheme, domain, path)

        message = EmailMessage(subject="auth link", to=[user.mail], body=link)
        message.send()
    return render(request, "login/request_link_ok.html",
                  {"mail": request.POST["mail"]})
