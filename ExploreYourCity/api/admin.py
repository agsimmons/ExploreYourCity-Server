from django.contrib import admin

from . import models

admin.site.register(models.Type)
admin.site.register(models.Category)
admin.site.register(models.Mission)
admin.site.register(models.Objective)
admin.site.register(models.Player)
admin.site.register(models.ObjectivePlayer)
admin.site.register(models.Request)
