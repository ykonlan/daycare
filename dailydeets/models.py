from django.db import models
from django.utils import timezone

class DailyDeets(models.Model):
    date = models.DateField(default=timezone.now)
    ward_id = models.ForeignKey("ward.ward",on_delete=models.CASCADE)
    meals = models.JSONField()
    naps = models.JSONField(null=True)
    medication = models.JSONField(null=True)
    day_highlight = models.CharField(max_length=150,null=True)
    extra_needs = models.CharField(max_length=100,null=True)
    general_mood = models.CharField(max_length=50,null=True)
    special_behavior = models.CharField(max_length=100,null=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["date","ward_id"],name="unique_ward_date")]