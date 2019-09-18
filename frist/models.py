from django.db import models


class Frist(models.Model):
    bezeichnung = models.CharField(max_length=50)
    zeitraum = models.DurationField()


class Pruefung(models.Model):
    frist = models.ForeignKey("Frist", on_delete=models.CASCADE)
    eintragung = models.DateField()
    ablauf = models.DateField()


class Fristzuordenbarkeit(models.Model):
    frist = models.ForeignKey("Frist", on_delete=models.CASCADE)
    rolle = models.ForeignKey("rolle.Rolle", on_delete=models.CASCADE)
