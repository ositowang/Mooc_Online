__author__ = 'osito_wang'
__date__ = '2018/6/30 11:16'

from django.conf.urls import url
from course.views import CourseListView

urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name="course_list")

]
