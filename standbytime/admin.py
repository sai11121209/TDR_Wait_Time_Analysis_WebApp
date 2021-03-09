from django.contrib import admin
from .models import (
    standbyTimeDataTDL,
    standbyTimeDataTDS,
    averageStandbyTimeDataTDL,
    averageStandbyTimeDataTDS,
)

# Register your models here.
# admin.site.register(Posts)
admin.site.register(standbyTimeDataTDL)
admin.site.register(standbyTimeDataTDS)
admin.site.register(averageStandbyTimeDataTDL)
admin.site.register(averageStandbyTimeDataTDS)
