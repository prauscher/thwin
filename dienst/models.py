from django.db import models


class Dienst(models.Model):
    datum = models.DateField()
    thema = models.TextField()
    gruppe = models.ForeignKey("gruppe.Gruppe", on_delete=models.CASCADE)

    def __str__(self):
        return "{:%Y-%m-%d} {}".format(self.datum, self.thema)


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
