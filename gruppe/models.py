from django.db import models


class Gruppe(models.Model):
    bezeichnung = models.CharField(max_length=20)
    uebergeordnet = models.ForeignKey("self", on_delete=models.CASCADE,
                                      related_name="untergeordnet",
                                      blank=True, null=True)

    def __str__(self):
        if self.uebergeordnet is None:
            return self.bezeichnung
        return "{} / {}".format(self.uebergeordnet, self.bezeichnung)
