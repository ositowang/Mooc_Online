from datetime import datetime

from django.db import models


class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name="city_name")
    desc = models.CharField(max_length=200, verbose_name="city_desc")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = "city"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name="organization_name")
    desc = models.TextField(verbose_name="organization_desc")
    click_num = models.IntegerField(default=0, verbose_name="click_num")
    fav_num = models.IntegerField(default=0, verbose_name="fav_num")
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name="organization_cover_image")
    address = models.CharField(max_length=150, verbose_name="organization_address")
    city = models.ForeignKey(CityDict, verbose_name="organization_city")
    category = models.CharField(max_length=20, verbose_name="org_category", default="company",
                                choices=(
                                    ("company", "Company"), ("university", "University"), ("individual", "Individual")))
    student_num = models.IntegerField(default=0, verbose_name="student_num")
    course_num = models.IntegerField(default=0, verbose_name="course_num")

    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = "course_organization"
        verbose_name_plural = verbose_name

    def get_teacher_num(self):
        """
        count the teacher numbers that belong to the organization
        :return: int teacher numbers
        """
        return self.teacher_set.all().count()

    def __str__(self):
        return self.name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name="teacher_organization")
    name = models.CharField(max_length=50, verbose_name="teacher_name")
    work_years = models.IntegerField(default=0, verbose_name="work_years")
    company = models.CharField(max_length=50, verbose_name="teacher_company")
    work_position = models.CharField(max_length=50, verbose_name="teacher_position")
    advantages = models.CharField(max_length=50, verbose_name="teacher_advantage")
    click_num = models.IntegerField(default=0, verbose_name="click_num")
    fav_num = models.IntegerField(default=0, verbose_name="fav_num")
    add_time = models.DateTimeField(default=datetime.now)
    image = models.ImageField(upload_to="teacher/%Y/%m", verbose_name="teacher_image", max_length=100, default="")

    class Meta:
        verbose_name = "teacher"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
