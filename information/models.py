from django.db import models
from django.utils import timezone

# Create your models here.
class Favorite(models.Model):
    class Meta:
        verbose_name = "全ユーザお気に入りアトラクション"
        verbose_name_plural = "全ユーザお気に入りアトラクションリスト"

    user = models.ForeignKey("auth.user", on_delete=models.CASCADE)
    park_type = models.TextField(max_length=10)
    facilityCode = models.TextField(max_length=10)
    submit_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Use:{self.user}　　　　ParkType:{self.park_type}　　　　FacilityCode:{self.facilityCode}　　　　SubmitTime:{str(self.submit_time)}"
