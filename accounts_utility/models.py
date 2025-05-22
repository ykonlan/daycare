from django.db import models
from django.contrib.auth.models import PermissionsMixin,AbstractBaseUser,BaseUserManager
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ValidationError

class CustomUserManager(BaseUserManager):
    def create_user(self,user_phone,email,name,password=None,**extra_fields):
        if not email or not user_phone or not name:
            raise ValueError("Name, email and phone are all required")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_staff",False)
        extra_fields.setdefault("is_active",True)
        user = self.model(user_phone=user_phone,email=email,name=name,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,user_phone,email,name,password=None,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        extra_fields.setdefault("is_active",True)
        return self.create_user(user_phone,email,name,password,**extra_fields)
    


class CustomUserModel(PermissionsMixin,AbstractBaseUser):
    user_phone = models.CharField(max_length=15,unique=True)
    email = models.EmailField(max_length=100,unique=True)
    name = models.CharField(max_length=155)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_added = models.DateField(default=timezone.now)

    objects = CustomUserManager()

    REQUIRED_FIELDS = ['name','user_phone']
    USERNAME_FIELD = 'email'

    def __str__(self):
        return f"{self.name}"
    

    

    

