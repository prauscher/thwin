from django.db import models


class Entitaet(models.Model):
    gruppe = models.ForeignKey("gruppe.Gruppe", on_delete=models.CASCADE)


class Person(Entitaet):
    mail = models.EmailField(blank=True, null=True)
    authCode = models.CharField(max_length=30, blank=True, null=True)
    name = models.CharField(max_length=50)


class Material(Entitaet):
    bezeichnung = models.CharField(max_length=70)


class Rollenzugehoerigkeit(models.Model):
    entitaet = models.ForeignKey("Entitaet", on_delete=models.CASCADE)
    rolle = models.ForeignKey("rolle.Rolle", on_delete=models.CASCADE)
    gruppe = models.ForeignKey("gruppe.Gruppe", on_delete=models.CASCADE)
    von = models.DateField()
    bis = models.DateField(blank=True, null=True)
