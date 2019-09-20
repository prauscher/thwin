from django.db import models
from model_utils.managers import InheritanceManager


class Entitaet(models.Model):
    objects = InheritanceManager()
    gruppe = models.ForeignKey("gruppe.Gruppe", on_delete=models.CASCADE,
                               related_name="entitaeten")


class Person(Entitaet):
    mail = models.EmailField(blank=True, null=True)
    auth_code = models.CharField(max_length=30, blank=True, null=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Material(Entitaet):
    bezeichnung = models.CharField(max_length=70)

    def __str__(self):
        return self.bezeichnung


class Rollenzugehoerigkeit(models.Model):
    entitaet = models.ForeignKey("Entitaet", on_delete=models.CASCADE,
                                 related_name="rollenzugehoerigkeiten")
    rolle = models.ForeignKey("rolle.Rolle", on_delete=models.CASCADE,
                              related_name="rollenzugehoerigkeiten")
    gruppe = models.ForeignKey("gruppe.Gruppe", on_delete=models.CASCADE,
                               related_name="rollenzugehoerigkeiten")
    von = models.DateField()
    bis = models.DateField(blank=True, null=True)

    def __str__(self):
        description = "{} ist {} in {}".format(self.entitaet, self.rolle,
                                               self.gruppe)
        if self.bis is None:
            description = description + " (seit {:%Y%m%d})".format(self.von)
        else:
            description = description + (" ({:%Y%m%d} - {:%Y%m%d})"
                                         .format(self.von, self.bis))

        return description
