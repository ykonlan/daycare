from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class StaffProfile(models.Model):
    staff_id = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="staff_profile")
    class_name = models.ForeignKey("ward.classes",on_delete=models.CASCADE)

    def clean(self):
        if not self.staff_id.groups.filter(name="staff").exists():
            raise ValidationError("Only staff can have a staff profile")
