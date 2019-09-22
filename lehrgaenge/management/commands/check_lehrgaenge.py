import requests
from lxml import html
from datetime import datetime, timedelta
import re

from django.core.management.base import BaseCommand
from django.utils import timezone

from lehrgaenge.models import Lehrgang, Teilnahme


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('--last-minute', action="store_true", help="Mailversand abhängig von verfügbaren Restplätzen")
        parser.add_argument('--daysleft', action="store_true", help="Mailversand abhängig von verbleibenden Tagen bis Lehrgangsbeginn")
        parser.add_argument('--mindaysleft', type=int, help="Keine Mail versenden, wenn weniger als x Tage bis Lehrgangsbeginn verbleiben", default=7*8)
        parser.add_argument('--maxdaysleft', type=int, help="Keine Mail versenden, wenn mehr als x Tage bis Lehrgangsbeginn verbleiben", default=7*10)

    def create_filter(self, last_minute, daysleft, mindaysleft, maxdaysleft):
        def _filter(termin_start, restplaetze):
            if last_minute and restplaetze > 0:
                return True

            restzeit = termin_start - datetime.now()
            if daysleft and (restzeit < timedelta(days=maxdaysleft) and restzeit > timedelta(days=mindaysleft)):
                return True

            return False
        return _filter

    def handle(self, last_minute, daysleft, mindaysleft, maxdaysleft, *args, **kwargs):
        filter = self.create_filter(last_minute, daysleft, mindaysleft, maxdaysleft)
        next = "SiteGlobals/Forms/Archiv/THW-BuS/DE/Lehrgangsangebote/Lehrgangsangebote_Formular.html"
        while True:
            next = self._handle("https://www.thw-bundesschule.de/", next, filter)
            if next is None:
                break

    def _handle(self, host, path, filter):
        tree = html.fromstring(requests.get(host + path, headers={"User-Agent": "TotallyNotRequests/1.1"}).content)
        for elem in tree.xpath('//div[@class="courseList"]//div[@class="teaser course"]'):
            titel_elem = elem.find("h2")
            if titel_elem.find("a") is not None:
                titel = titel_elem.find("a").text
                link = host + titel_elem.find("a").get("href")
            else:
                titel = titel_elem.text
                link = None
            termin_start = datetime.strptime(elem.findall('dl[@class="docData"]//dd')[0].text[4:], "%d.%m.%Y, %H:%M Uhr")
            termin_ende = datetime.strptime(elem.findall('dl[@class="docData"]//dd')[1].text[4:], "%d.%m.%Y, %H:%M Uhr")
            restplaetze = 0
            if elem.find('p[@class="courseAction"]//a') is not None:
                scan_text = elem.find('p[@class="courseAction"]//a').text
                match = re.match(r'Noch (\d+) Last-Minute-Plätze verfügbar', scan_text)
                if match is not None:
                    restplaetze = int(match.group(1))

            self._handle_lehrgang(titel, link, termin_start, termin_ende, restplaetze, filter)

        next = tree.xpath('//ul[@class="right presearch"]//li[@class="forward"]//a')
        if not next:
            return None
        return next[0].get("href")

    def _handle_lehrgang(self, titel, link, termin_start, termin_ende, restplaetze, filter):
        # normalisieren
        kuerzel, bezeichnung = [text.strip() for text in titel.split("-", 1)]
        kuerzel = "".join([char for char in kuerzel if char.isalnum()]).capitalize()
        austragung = Lehrgang.BUNDESSCHULE

        lehrgang, _ = Lehrgang.objects.get_or_create(kuerzel=kuerzel, austragung=austragung, defaults={"name": bezeichnung})
        lehrgang.name = bezeichnung
        lehrgang.link = link
        lehrgang.save()

        # wenn meldefrist bevorsteht alarmieren
        if filter(termin_start, restplaetze):
            for teilnahme in lehrgang.teilnahmen.exclude(status=Teilnahme.BESUCHT):
                # TODO mail an teilnehmer schicken
                print(teilnahme, link)
