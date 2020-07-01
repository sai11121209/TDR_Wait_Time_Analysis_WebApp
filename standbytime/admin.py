from django.contrib import admin
from .models import standbyTimeDataTDL, standbyTimeDataTDS
from markdownx.admin import MarkdownxModelAdmin

# Register your models here.
# admin.site.register(Posts)
admin.site.register(standbyTimeDataTDL, MarkdownxModelAdmin)
admin.site.register(standbyTimeDataTDS, MarkdownxModelAdmin)
