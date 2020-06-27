from django.db import models
from django.utils import timezone

# Create your models here.


class standbyTimeData(models.Model):
    facility_code = models.IntegerField()
    standby_time = models.IntegerField(null=True)
    time = models.TimeField(default=timezone.now)
    operating_status = models.CharField(null=True, max_length=60)
    operating_status_start = models.TimeField(null=True)
    operating_status_end = models.TimeField(null=True)
    facility_fastpass_status = models.CharField(null=True, max_length=60)
    facility_fastpass_start = models.TimeField(null=True)
    facility_fastpass_end = models.TimeField(null=True)

    def __str__(self):
        return str(self.pk)
