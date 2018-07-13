import json

from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q

from .models import CourseOrg, CityDict, Teacher
from .forms import UserQuestionForm
from course.models import Course
from operation.models import UserFavorite


# Create your views here.


class OrgView(View):
    """
    Course Organization List Module
    """

    def get(self, request):
        # Course Organization
        all_orgs = CourseOrg.objects.all()
        # Get the hottest 3 organizations
        hot_orgs = all_orgs.order_by("-click_num")[:3]

        # Search by Organization
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))

        # Filter by city
        city_id = request.GET.get("city", "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # Filter by category
        category = request.GET.get("ct", "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        # Sort the result by student numbers and course numbers
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-student_num")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_num")
        # Count the total organizations got
        org_nums = all_orgs.count()

        # Enables Pagination function
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 5, request=request)

        orgs = p.page(page)

        # City
        all_cities = CityDict.objects.all()
        return render(request, "org_list.html",
                      {"all_orgs": orgs,
                       "all_cities": all_cities,
                       "org_nums": org_nums,
                       "city_id": city_id,
                       "category": category,
                       "hot_orgs": hot_orgs,
                       "sort": sort})


class AddUserQuestionView(View):
    """
    User Quote about Courses
    """

    def post(self, request):
        userquestion_form = UserQuestionForm(request.POST)
        if userquestion_form.is_valid():
            user_question = userquestion_form.save(commit=True)
            success_dict = {"status": "success"}
            return HttpResponse(json.dumps(success_dict), content_type='application/json')
        else:
            fail_dict = {"status": "fail", "msg": "{0}".format(userquestion_form.errors)}
            return HttpResponse(json.dumps(fail_dict),
                                content_type='application/json')


class OrgHomeView(View):
    """
    Organization Home Page
    """

    def get(self, request, org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_num += 1
        course_org.save()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()
        all_teachers = course_org.teacher_set.all()
        return render(request, "org-detail-homepage.html",
                      {"all_courses": all_courses, "all_teachers": all_teachers, "course_org": course_org,
                       "current_page": current_page, "has_fav": has_fav})


class OrgCourseView(View):
    """
    Organization Course List Page
    """

    def get(self, request, org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()
        return render(request, "org-detail-course.html",
                      {"all_courses": all_courses, "course_org": course_org, "current_page": current_page,
                       "has_fav": has_fav})


class OrgDescView(View):
    """
    Organization Description Page
    """

    def get(self, request, org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, "org-detail-desc.html",
                      {"course_org": course_org, "current_page": current_page, "has_fav": has_fav})


class OrgTeacherView(View):
    """
    Organization Teacher List Page
    """

    def get(self, request, org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_teachers = course_org.teacher_set.all()
        return render(request, "org-detail-teachers.html",
                      {"all_teachers": all_teachers, "course_org": course_org, "current_page": current_page,
                       "has_fav": has_fav})


class AddFavView(View):
    """
    User Add Favorite and Cancel Favorite Function
    """

    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        if not request.user.is_authenticated():
            # Check if the user is login or not
            return HttpResponse('{"status": "fail", "msg": "User is not login"}',
                                content_type='application/json')
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            exist_records.delete()
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_num -= 1
                if course.fav_num < 0:
                    course.fav_num = 0
                course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_num -= 1
                if course_org.fav_num < 0:
                    course_org.fav_num = 0
                course_org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_num -= 1
                if teacher.fav_num < 0:
                    teacher.fav_num = 0
                teacher.save()
            return HttpResponse('{"status": "success", "msg": "Favorite"}',
                                content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_num += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_num += 1
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_num += 1
                    teacher.save()
                return HttpResponse('{"status": "success", "msg": "Favored"}',
                                    content_type='application/json')
            else:
                return HttpResponse('{"status": "fail", "msg": "Fail to Favorite"}',
                                    content_type='application/json')


class TeacherListView(View):
    """
    Teacher  List Page
    """

    def get(self, request):
        all_teachers = Teacher.objects.all()
        # Sort the result by student numbers and course numbers
        sort = request.GET.get('sort', "")

        # Search by Teacher
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=search_keywords) |
                                               Q(company__icontains=search_keywords) |
                                               Q(work_position__icontains=search_keywords))
        if sort:
            if sort == "hot":
                all_teachers = all_teachers.order_by("-click_num")

        sorted_teacher = Teacher.objects.all().order_by("-click_num")[:3]
        # Enables Pagination function
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teachers, 1, request=request)

        teachers = p.page(page)
        return render(request, "teachers-list.html",
                      {"all_teachers": teachers, "sorted_teacher": sorted_teacher, "sort": sort})


class TeacherDetailView(View):
    """
    Teacher Detail Page
    """

    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_num += 1
        teacher.save()
        all_courses = Course.objects.filter(teacher=teacher)
        # Teachers Ranking
        sorted_teacher = Teacher.objects.all().order_by("-click_num")[:3]

        has_teacher_favored = False
        if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
            has_teacher_favored = True
        has_org_favored = False
        if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
            has_org_favored = True

        return render(request, "teacher-detail.html",
                      {"teacher": teacher, "all_courses": all_courses, "sorted_teacher": sorted_teacher,
                       "has_teacher_favored": has_teacher_favored, "has_org_favored": has_org_favored})
