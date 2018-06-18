__author__ = 'osito_wang'
__date__ = '2018/6/15 14:08'
import xadmin

from .models import Course, Chapter, Video, CourseResource


class CourseAdmin(object):
    list_display = ["name", "degree", "learn_time", "students_num", "fav_num", "image", "click_num", "add_time"]
    search_fields = ["name", "degree", "learn_time", "students_num", "fav_num", "image", "click_num"]
    list_filter = ["name", "degree", "learn_time", "students_num", "fav_num", "click_num", "add_time"]


class ChapterAdmin(object):
    list_display = ["course", "name", "add_time"]
    search_fields = ["course", "name"]
    list_filter = ["course__name", "name", "add_time"]


class VideoAdmin(object):
    list_display = ["chapter", "name", "add_time"]
    search_fields = ["chapter", "name"]
    list_filter = ["chapter__name", "name", "add_time"]


class CourseResourceAdmin(object):
    list_display = ["course", "name", "download", "add_time"]
    search_fields = ["course", "name", "download", ]
    list_filter = ["course__name", "name", "download", "add_time"]


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Chapter, ChapterAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
