from datetime import datetime

from django.db import models

from users.models import UserProfile
from course.models import Course


# Create your models here.

class UserQuestion(models.Model):
    name = models.CharField(max_length=20, verbose_name="user_name")
    mobile = models.CharField(max_length=11, verbose_name="user_mobile")
    course_name = models.CharField(max_length=50, verbose_name="course_name")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="add_time")

    class Meta:
        verbose_name = "user_question"
        verbose_name_plural = verbose_name


class CourseComments(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="user")
    course = models.ForeignKey(Course, verbose_name="course")
    comments = models.CharField(max_length=200, verbose_name="comments")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="add_time")

    class Meta:
        verbose_name = "course_comments"
        verbose_name_plural = verbose_name


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="user")
    fav_id = models.IntegerField(default=0, verbose_name="fav_id")
    fav_type = models.IntegerField(choices=((1, "Course"), (2, "Organization"), (3, "Teacher")), default=1,
                                   verbose_name="fav_type")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="add_time")

    class Meta:
        verbose_name = "user_favorite"
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name="accepting_user")
    message = models.CharField(max_length=300, verbose_name="message_content")
    has_read = models.BooleanField(max_length=False, verbose_name="read_status")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="add_time")

    class Meta:
        verbose_name = "user_message"
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="user")
    course = models.ForeignKey(Course, verbose_name="course")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="add_time")

    class Meta:
        verbose_name = "user_course"
        verbose_name_plural = verbose_name
