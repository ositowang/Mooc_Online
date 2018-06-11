from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, default="", verbose_name="nick_name")
    birthday = models.DateField(verbose_name="birthday", null=True, blank=True)
    gender = models.CharField(choices=(("male", "male"), ("female", "female")), default="female",max_length=20)
    address = models.CharField(max_length=100, default="")
    mobile = models.CharField(max_length=15, null=True, blank=True)
    profile_image = models.ImageField(upload_to="image/%Y/%m", default="image/default.png", max_length=100)

    class Meta:
        verbose_name = "user_profile"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
