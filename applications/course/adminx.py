__author__ = 'osito_wang'
__date__ = '2018/6/15 14:08'
import xadmin

from .models import Course, Chapter, Video, CourseResource, BannerCourse


class ChapterInline(object):
    model = Chapter
    extra = 0


class CourseResourceInline(object):
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    list_display = ["name", "degree", "learn_time", "students_num", "detail", "fav_num", "image", "click_num",
                    "add_time", "tag", "teacher", "get_chapter_num"]
    search_fields = ["name", "degree", "learn_time", "students_num", "fav_num", "image", "click_num", "tag",
                     "teacher", ]
    list_filter = ["name", "degree", "learn_time", "students_num", "fav_num", "click_num", "add_time", "tag", "teacher"]
    readonly_fields = ["students_num", "fav_num", "click_num"]
    list_editable = ['degree', 'desc']
    ordering = ['-click_num']
    style_fields = {"detail": "ueditor"}
    inlines = [ChapterInline, CourseResourceInline]
    import_excel = True

    def queryset(self):
        """
        filter the banner course
        :return: courses not banner one queryset
        """
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):
        """
        Update the course numbers of a course organization when a course is saved
        :return:
        """
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()

    def post(self, request, *args, **kwargs):
        """
        Excel Addons
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if 'excel' in request.FILES:
            pass
        return super(CourseAdmin, self).post(request, args, kwargs)


class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students_num']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students_num']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students_num']
    ordering = ['-click_num']
    readonly_fields = ['click_num']
    exclude = ['fav_num']
    inlines = [ChapterInline, CourseResourceInline]

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


class ChapterAdmin(object):
    list_display = ["course", "name", "add_time"]
    search_fields = ["course", "name"]
    list_filter = ["course__name", "name", "add_time"]


class VideoAdmin(object):
    list_display = ["chapter", "name", "add_time", "url", "video_duration"]
    search_fields = ["chapter", "name", "video_link"]
    list_filter = ["chapter__name", "name", "add_time", "url", "video_duration"]


class CourseResourceAdmin(object):
    list_display = ["course", "name", "download", "add_time"]
    search_fields = ["course", "name", "download", ]
    list_filter = ["course__name", "name", "download", "add_time"]


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Chapter, ChapterAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
