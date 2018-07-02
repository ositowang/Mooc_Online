from django.shortcuts import render
from django.views.generic.base import View

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course


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
