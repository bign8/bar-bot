from django.contrib import admin
from . import models

admin.site.register(models.Ingredient)
admin.site.register(models.Recipe)
admin.site.register(models.Amount)
admin.site.register(models.Comment)