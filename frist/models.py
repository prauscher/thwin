from django.db import models


class Frist(models.Model):
    bezeichnung = models.CharField(max_length=50)
    zeitraum = models.DurationField(blank=True, null=True)

    def __str__(self):
        return self.bezeichnung


class Pruefung(models.Model):
    frist = models.ForeignKey("Frist", on_delete=models.CASCADE,
                              related_name="pruefungen")
    eintragung = models.DateField()
    ablauf = models.DateField()

    def __str__(self):
        return "{} ({})".format(self.frist, self.eintragung)


class Fristzuordenbarkeit(models.Model):
    frist = models.ForeignKey("Frist", on_delete=models.CASCADE,
                              related_name="zuordenbarkeiten")
    rolle = models.ForeignKey("rolle.Rolle", on_delete=models.CASCADE,
                              related_name="fristzuordenbarkeiten")

    def __str__(self):
        return "{} für {}".format(self.frist, self.rolle)
