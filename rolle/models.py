from django.db import models


class Berechtigung(models.Model):
    bezeichnung = models.CharField(max_length=50)

    def __str__(self):
        return self.bezeichnung


class Rolle(models.Model):
    bezeichnung = models.CharField(max_length=40)

    def __str__(self):
        return self.bezeichnung


class Freigabe(models.Model):
    berechtigung = models.ForeignKey("Berechtigung", on_delete=models.CASCADE)
    rolle = models.ForeignKey("Rolle", on_delete=models.CASCADE)
    untergruppen = models.BooleanField()

    def __str__(self):
        format_string = "{} darf {}"
        if self.untergruppen:
            format_string = format_string + " inkl. Untergruppen"

        return format_string.format(self.rolle, self.berechtigung)
