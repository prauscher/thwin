from django.db import models


class Gruppe(models.Model):
    bezeichnung = models.CharField(max_length=20)
    uebergeordnet = models.ForeignKey("self", on_delete=models.CASCADE)
