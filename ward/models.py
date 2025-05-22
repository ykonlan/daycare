from django.db import models
from django.utils import timezone
from django.conf import settings


class Classes(models.Model):
    class_name = models.CharField(max_length=20,primary_key=True)
    class_population = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.class_name


class Ward(models.Model):
    name = models.CharField(max_length=90)
    date_added = models.DateField(default=timezone.now)
    date_of_birth = models.DateField()
    parent_id = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="wards")
    class_name = models.ForeignKey("classes",on_delete=models.SET_NULL,null=True)


    def save(self,*args,**kwargs):
        is_new = self._state.adding
        if not is_new:
            old_class = Ward.objects.get(id=self.id).class_name
            super().save()
            new_class = self.class_name
            if old_class != new_class:
                old_class.class_population -= 1
                old_class.save()
                new_class.class_population += 1
                new_class.save()
        else:
            if self.class_name:
                super().save()
                self.class_name.class_population += 1
                self.class_name.save()
            

    def delete(self,*args,**kwargs):
       ward_class = self.class_name
       super().delete()
       ward_class.class_population -= 1
       ward_class.save()


class Allergies(models.Model):
    allergy_name = models.CharField(max_length=50)
    allergy_reaction = models.CharField(max_length=50)
    CHOICES = [("high","High"),("moderate","Moderate"),("low","Low")]
    allergy_severity = models.CharField(choices=CHOICES)
    ward_id = models.ForeignKey("ward",on_delete=models.CASCADE)

