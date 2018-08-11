from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField

from organization.models import CourseOrg, Teacher


# Course basic model
class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name="course_organization", null=True, blank="True")
    name = models.CharField(max_length=50, verbose_name="course_name")
    desc = models.CharField(max_length=300, verbose_name="course_desc")
    detail = UEditorField(verbose_name=u"course_detail", width=600, height=300, imagePath="courses/ueditor/",
                          filePath="courses/ueditor/", default='')
    degree = models.CharField(verbose_name="course_degree",
                              choices=(
                                  ("entry", "Elementary"), ("intermediate", "Junior"),
                                  ("advanced", "Advanced")),
                              max_length=20)
    learn_time = models.IntegerField(default=0, verbose_name="learning_time")
    teacher = models.ForeignKey(Teacher, verbose_name="instructor", null=True, blank=True)
    students_num = models.IntegerField(default=0, verbose_name="students_num")
    fav_num = models.IntegerField(default=0, verbose_name="fav_num")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name="cover_image")
    click_num = models.IntegerField(default=0, verbose_name="click_num")
    category = models.CharField(max_length=20, default="Back-End", verbose_name="course_category")
    tag = models.CharField(default="", verbose_name="course_tag", max_length=10)
    youneed_know = models.CharField(max_length=300, default="", verbose_name="course_needknow")
    teacher_tell = models.CharField(max_length=300, default="", verbose_name="teacher_tell")
    is_banner = models.BooleanField(default=False, verbose_name="is_banner")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="add_time")

    class Meta:
        verbose_name = "course"
        verbose_name_plural = verbose_name

    def get_chapter_num(self):
        """
        Count the chapter numbers in a course
        :return: int chapter numbers
        """
        return self.chapter_set.all().count()

    def get_learn_user(self):
        """
        Retrieve the 5 users who are learning the course
        :return: object UserCourse
        """
        return self.usercourse_set.all()[:5]

    def get_course_chapter(self):
        """
        Retrieve the course chapters
        :return: chapter queryset
        """
        return self.chapter_set.all()

    get_course_chapter.short_description = "Chapter Num"

    def __str__(self):
        return self.name


class BannerCourse(Course):
    class Meta:
        verbose_name = "Banner Course"
        verbose_name_plural = verbose_name
        proxy = True


# Course Chapter model
class Chapter(models.Model):
    course = models.ForeignKey(Course, verbose_name="chapter")
    name = models.CharField(max_length=100, verbose_name="chapter_name")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="add_time")

    class Meta:
        verbose_name = "course_chapter"
        verbose_name_plural = verbose_name

    def get_chapter_video(self):
        """
        Retrieve the chapter videos
        :return: queryset video
        """
        return self.video_set.all()

    def __str__(self):
        return self.name


# Chapter video model
class Video(models.Model):
    chapter = models.ForeignKey(Chapter, verbose_name="chapter_video")
    name = models.CharField(max_length=100, verbose_name="video_name")
    url = models.URLField(max_length=200, default="", verbose_name="video_link")
    video_duration = models.IntegerField(default=0, verbose_name="video_duration")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="add_time")

    class Meta:
        verbose_name = "course_video"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# Course Resource Model
class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name="course")
    name = models.CharField(max_length=100, verbose_name="name")
    download = models.FileField(upload_to="course/resource/%Y/%m", verbose_name="resource_file", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="add_time")

    class Meta:
        verbose_name = "course_resource"
        verbose_name_plural = verbose_name
