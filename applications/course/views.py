from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from operation.models import UserFavorite, CourseComments, UserCourse
from .models import Course, CourseResource, Video
from utils.mixin_utils import LoginRequiredMixin


# Create your views here.


class CourseListView(View):
    """
    Course List View
    """

    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")

        hot_courses = Course.objects.all().order_by("-click_num")[:3]

        # Sort the result by student numbers and course numbers
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students_num")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_num")
        # Enables Course Pagination function
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 3, request=request)
        courses = p.page(page)
        return render(request, "course-list.html", {"all_courses": courses,
                                                    "sort": sort,
                                                    "hot_courses": hot_courses})


class CourseDetailView(View):
    """
    Course detail Page View
    """

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # Whether the course has been favored
        has_fav_course = False
        # whether the course organization has been favored
        has_fav_org = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True

            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        tag = course.tag
        if tag:
            related_courses = Course.objects.filter(tag=tag)[:1]
        else:
            related_courses = []
        return render(request, "course-detail.html",
                      {"course": course, "related_courses": related_courses, "has_fav_course": has_fav_course,
                       "has_fav_org": has_fav_org})


class CourseInfoView(LoginRequiredMixin, View):
    """
    Course chapter Information
    """

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # Whether the course has been linked with the user
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        # Retrieve those users who are has learned this course
        user_incourse = UserCourse.objects.filter(course=course)
        user_ids = [course_user.user.id for course_user in user_incourse]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # Retrieve all courses ids and all the courses for those users who learned this course
        course_ids = [course.course.id for course in all_user_courses]
        related_courses = Course.objects.filter(id__in=course_ids).order_by("-click_num")[:5]
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, "course-video.html",
                      {"course": course, "course_resources": all_resources, "related_courses": related_courses})


class CommentsView(View):
    """
    Course Comment Page View
    """

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.filter(course=course).order_by("-id")
        return render(request, "course-comment.html", {
            "course": course,
            "course_resources": all_resources,
            "all_comments": all_comments
        })


class AddCommentView(View):
    """
    User Publish Comments View
    """

    def post(self, request):

        if not request.user.is_authenticated():
            # 判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"You need to Login First"}', content_type='application/json')
        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")
        if int(course_id) > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success", "msg":"Successfully post your comments"}',
                                content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"Fail to post your comments"}',
                                content_type='application/json')


class VideoPlayView(View):
    """
    Course Video Play Page
    """

    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.chapter.course
        # Whether the course has been linked with the user
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        # Retrieve those users who are has learned this course
        user_incourse = UserCourse.objects.filter(course=course)
        user_ids = [course_user.user.id for course_user in user_incourse]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # Retrieve all courses ids and all the courses for those users who learned this course
        course_ids = [course.course.id for course in all_user_courses]
        related_courses = Course.objects.filter(id__in=course_ids).order_by("-click_num")[:5]
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, "course-play.html",
                      {"course": course, "course_resources": all_resources, "related_courses": related_courses,
                       "video": video})
