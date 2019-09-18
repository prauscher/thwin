from django.contrib import admin
from . import models


admin.site.register(models.Berechtigung)
admin.site.register(models.Freigabe)
admin.site.register(models.Rolle)
