from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


# User Model
class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, default="", verbose_name="nick_name")
    birthday = models.DateField(verbose_name="birthday", null=True, blank=True)
    gender = models.CharField(choices=(("male", "Male"), ("female", "Female")), default="female", max_length=10)
    address = models.CharField(max_length=100, default="")
    mobile = models.CharField(max_length=15, null=True, blank=True)
    profile_image = models.ImageField(upload_to="image/%Y/%m", default="image/default.png", max_length=100)

    class Meta:
        verbose_name = "user_profile"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def unread_nums(self):
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id, has_read=False).count()


# Email Verify code model
class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name="verify_code")
    email = models.EmailField(max_length=50, verbose_name="user_email")
    send_type = models.CharField(
        choices=(("register", "New_User"), ("forget", "Forget_Password"), ("update", "Update_Email")), max_length=20)
    send_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = "email_verifycode"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}:{1}'.format(self.code, self.email)


# Banner Model
class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name="title")
    image = models.ImageField(upload_to="banner/%Y/%m", verbose_name="banner_image", max_length=100)
    url = models.URLField(max_length=200, verbose_name="image_url")
    index = models.IntegerField(default=100, verbose_name="image_sequence")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="add_time")

    class Meta:
        verbose_name = "banner"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
