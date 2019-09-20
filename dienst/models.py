from django.db import models


class Dienst(models.Model):
    start = models.DateTimeField()
    ende = models.DateTimeField()
    thema = models.TextField()
    gruppe = models.ForeignKey("gruppe.Gruppe", on_delete=models.CASCADE)

    def __str__(self):
        return "{:%Y-%m-%d} {} ({})".format(self.start, self.thema,
                                            self.gruppe)


class Teilnahme(models.Model):
    ANWESEND = "x"
    ABWESEND = "-"
    UNKLAR = "?"
    OPTIONS = [(ANWESEND, "Anwesend"),
               (ABWESEND, "Abwesend"),
               (UNKLAR, "Unklar")]

    dienst = models.ForeignKey('dienst.Dienst', on_delete=models.CASCADE)
    person = models.ForeignKey('entitaet.Person', on_delete=models.CASCADE)
    vorab = models.CharField(
        max_length=1, choices=OPTIONS, default=UNKLAR)
    ist = models.CharField(
        max_length=1, choices=OPTIONS, default=UNKLAR)

    def __str__(self):
        return "{} bei {}: {} vorab, {} ist".format(self.person, self.dienst,
                                                    self.vorab, self.ist)
