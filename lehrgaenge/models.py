from django.db import models


class Lehrgang(models.Model):
    BUNDESSCHULE = "b"
    REGIONAL = "r"
    OPTIONS = [(BUNDESSCHULE, "Bundesschule"),
               (REGIONAL, "Regionalbereich")]

    name = models.CharField(max_length=40)
    kuerzel = models.CharField(max_length=10)
    austragung = models.CharField(max_length=1, choices=OPTIONS)

    def __str__(self):
        return "{}: {}".format(self.kuerzel, self.name)


class Teilnahme(models.Model):
    WUNSCH_PRIORISIERT = "p"
    WUNSCH_OPTIONAL = "o"
    WUNSCH_INFO = "i"
    BESUCHT = "b"
    OPTIONS = [(WUNSCH_PRIORISIERT, "Priorisiert gewünscht"),
               (WUNSCH_OPTIONAL, "Gewünscht wenn möglich"),
               (WUNSCH_INFO, "Nur Last-Minute"),
               (BESUCHT, "Besucht")]

    lehrgang = models.ForeignKey('Lehrgang', on_delete=models.CASCADE)
    person = models.ForeignKey('entitaet.Person', on_delete=models.CASCADE,
                               related_name="lehrgang_teilnahmen")
    status = models.CharField(max_length=1, choices=OPTIONS,
                              default=WUNSCH_INFO)

    def __str__(self):
        return "{} bei {}: {}".format(self.person, self.lehrgang, self.status)
