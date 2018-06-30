from datetime import datetime

from django.db import models

from organization.models import CourseOrg


# Course basic model
class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name="course_organization", null=True, blank="True")
    name = models.CharField(max_length=50, verbose_name="course_name")
    desc = models.CharField(max_length=300, verbose_name="course_desc")
    detail = models.TextField(verbose_name="course_detail")
    degree = models.CharField(verbose_name="course_degree",
                              choices=(
                                  ("entry", "entry_level"), ("intermediate", "mid_level"),
                                  ("advanced", "advanced_level")),
                              max_length=20)
    learn_time = models.IntegerField(default=0, verbose_name="learning_time")
    students_num = models.IntegerField(default=0, verbose_name="students_num")
    fav_num = models.IntegerField(default=0, verbose_name="fav_num")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name="cover_image")
    click_num = models.IntegerField(default=0, verbose_name="click_num")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="add_time")

    class Meta:
        verbose_name = "course"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# Course Chapter model
class Chapter(models.Model):
    course = models.ForeignKey(Course, verbose_name="chapter")
    name = models.CharField(max_length=100, verbose_name="chapter_name")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="add_time")

    class Meta:
        verbose_name = "course_chapter"
        verbose_name_plural = verbose_name


# Chapter video model
class Video(models.Model):
    chapter = models.ForeignKey(Chapter, verbose_name="chapter_video")
    name = models.CharField(max_length=100, verbose_name="video_name")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="add_time")

    class Meta:
        verbose_name = "course_video"
        verbose_name_plural = verbose_name


# Course Resource Model
class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name="course")
    name = models.CharField(max_length=100, verbose_name="name")
    download = models.FileField(upload_to="course/resource/%Y/%m", verbose_name="resource_file", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="add_time")

    class Meta:
        verbose_name = "course_resource"
        verbose_name_plural = verbose_name
