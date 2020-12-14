from django.db import models
from django.utils import timezone

# Create your models here.


class standbyTimeDataTDL(models.Model):
    class Meta:
        verbose_name = "東京ディズニーランド待ち時間データ"
        verbose_name_plural = "東京ディズニーランド待ち時間データリスト"

    facilityCode = models.TextField(max_length=10)
    standby_time = models.FloatField(null=True)
    time = models.DateTimeField(default=timezone.now)
    operating_status = models.CharField(null=True, max_length=60)
    operating_status_start = models.TimeField(null=True)
    operating_status_end = models.TimeField(null=True)
    facility_fastpass_status = models.CharField(null=True, max_length=60)
    facility_fastpass_start = models.TimeField(null=True)
    facility_fastpass_end = models.TimeField(null=True)

    def __str__(self):
        return f"ID:{str(self.pk)}　　　　FacilityCode:{self.facilityCode}　　　　Time:{str(self.time)}"


class standbyTimeDataTDS(models.Model):
    class Meta:
        verbose_name = "東京ディズニーシー待ち時間データ"
        verbose_name_plural = "東京ディズニーシー待ち時間データリスト"

    facilityCode = models.TextField(max_length=10)
    standby_time = models.FloatField(null=True)
    time = models.DateTimeField(default=timezone.now)
    operating_status = models.CharField(null=True, max_length=60)
    operating_status_start = models.TimeField(null=True)
    operating_status_end = models.TimeField(null=True)
    facility_fastpass_status = models.CharField(null=True, max_length=60)
    facility_fastpass_start = models.TimeField(null=True)
    facility_fastpass_end = models.TimeField(null=True)

    def __str__(self):
        return f"ID:{str(self.pk)}　　　　FacilityCode:{self.facilityCode}　　　　Time:{str(self.time)}"


class averageStandbyTimeDataTDL(models.Model):
    class Meta:
        verbose_name = "東京ディズニーランド平均待ち時間データ"
        verbose_name_plural = "東京ディズニーランド平均待ち時間データリスト"

    facilityCode = models.TextField(max_length=10)
    standby_time = models.FloatField(null=True)
    time = models.TimeField()

    def __str__(self):
        return f"ID:{str(self.pk)}　　　　FacilityCode:{self.facilityCode}　　　　Time:{str(self.time)}　　　　StadbyTime:{str(self.standby_time)}"


class averageStandbyTimeDataTDS(models.Model):
    class Meta:
        verbose_name = "東京ディズニーシー平均待ち時間データ"
        verbose_name_plural = "東京ディズニーシー平均待ち時間データリスト"

    facilityCode = models.TextField(max_length=10)
    standby_time = models.FloatField(null=True)
    time = models.TimeField()

    def __str__(self):
        return f"ID:{str(self.pk)}　　　　FacilityCode:{self.facilityCode}　　　　Time:{str(self.time)}　　　　StadbyTime:{str(self.standby_time)}"
