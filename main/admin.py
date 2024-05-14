from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Userdata)
admin.site.register(models.Category)
admin.site.register(models.Nums)
admin.site.register(models.Otherlink)
admin.site.register(models.Sociallink)
admin.site.register(models.Platform)
admin.site.register(models.Nin)
admin.site.register(models.Ristriction)

