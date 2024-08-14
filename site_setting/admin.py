from django.contrib import admin
from . import models

class AdminBanneers (admin.ModelAdmin):
    list_display = ['title','position','is_active']
    list_editable = ['is_active']


admin.site.register(models.SiteBanner,AdminBanneers)
admin.site.register(models.SiteSettings)
admin.site.register(models.SiteFooter)
admin.site.register(models.Link_Boxes)
admin.site.register(models.q_and_answer)

