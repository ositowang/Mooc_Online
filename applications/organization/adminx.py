__author__ = 'osito_wang'
__date__ = '2018/6/15 14:29'
import xadmin

from .models import CourseOrg, CityDict, Teacher


class CourseOrgAdmin(object):
    list_display = ["name", "desc", "click_num", "fav_num", "image", "address", "city", "add_time"]
    search_fields = ["name", "click_num", "fav_num", "address", "city"]
    list_filter = ["name", "click_num", "fav_num", "address", "city", "add_time"]


class CityDictAdmin(object):
    list_display = ["name", "desc", "add_time"]
    search_fields = ["name", "desc"]
    list_filter = ["name", "desc", "add_time"]


class TeacherAdmin(object):
    list_display = ["org", "name", "work_years", "company", "work_position", "advantages", "click_num", "fav_num",
                    "add_time"]
    search_fields = ["org", "name", "work_years", "company", "work_position", "advantages", "click_num", "fav_num"]
    list_filter = ["org", "name", "work_years", "company", "work_position", "advantages", "click_num", "fav_num",
                   "add_time"]


xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
