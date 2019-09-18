from django.db import models


class Berechtigung(models.Model):
    bezeichnung = models.CharField(max_length=50)


class Rolle(models.Model):
    bezeichnung = models.CharField(max_length=40)


class Freigabe(models.Model):
    berechtigung = models.ForeignKey("Berechtigung", on_delete=models.CASCADE)
    rolle = models.ForeignKey("Rolle", on_delete=models.CASCADE)
    untergruppen = models.BooleanField()
