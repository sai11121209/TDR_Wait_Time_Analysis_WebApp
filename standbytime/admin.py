from django.contrib import admin
from .models import standbyTimeDataTDL, standbyTimeDataTDS

# Register your models here.
# admin.site.register(Posts)
admin.site.register(standbyTimeDataTDL)
admin.site.register(standbyTimeDataTDS)
