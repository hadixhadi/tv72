from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import CustomUserManager
from django.utils import timezone
from datetime import timedelta

# Create your models here.

class User(AbstractBaseUser):
    TYPE=[
        (1,'UNIVERSITY STUDENT'),
        (2,'COLLAGE STUDENT'),
        (3,'EMPLOYER'),
        (4,"SUPER ADMIN")
    ]
    #required fields
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    national_code=models.CharField(max_length=10,unique=True,primary_key=True)
    phone_number=models.CharField(max_length=11,unique=True,null=True,blank=True)
    type = models.SmallIntegerField(choices=TYPE, null=True, blank=True)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['national_code', 'first_name', 'last_name']
    is_super_admin=models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    phone_active = models.BooleanField(default=False)
    objects=CustomUserManager()

    def __str__(self):
        return f"{self.first_name} - {self.last_name} - {self.national_code}"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin



class UserProfile(models.Model):
    user=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="user_profile")

    father_name = models.CharField(max_length=200, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    education = models.CharField(max_length=200, null=True, blank=True)
    telephone = models.CharField(max_length=11, null=True, blank=True)

    registered_at=models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.user.first_name


class OtpCode(models.Model):
    phone_number=models.CharField(max_length=11,unique=True)
    code=models.PositiveSmallIntegerField()
    created_time=models.DateTimeField(auto_now_add=True)
    expire_at=models.TimeField(null=True,blank=True)
    def set_expire_time(self):
        self.expire_at=timezone.now() + timedelta(minutes=2)
        self.save()
    def __str__(self):
        return f"{self.phone_number} - {self.code} - {self.created_time}"