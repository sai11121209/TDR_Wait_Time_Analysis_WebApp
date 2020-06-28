from django.db import models
from django.utils import timezone

# Create your models here.


class standbyTimeData(models.Model):
    facility_code = models.IntegerField()
    standby_time = models.IntegerField(null=True)
    time = models.DateTimeField(default=timezone.now)
    operating_status = models.CharField(null=True, max_length=60)
    operating_status_start = models.DateTimeField(null=True)
    operating_status_end = models.DateTimeField(null=True)
    facility_fastpass_status = models.CharField(null=True, max_length=60)
    facility_fastpass_start = models.DateTimeField(null=True)
    facility_fastpass_end = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.pk)
