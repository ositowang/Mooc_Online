import json

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from users.models import UserProfile, EmailVerifyRecord,Banner
from users.forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, UploadImageForm, UserInfoForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from course.models import Course


class CustomBackend(ModelBackend):
    """
    Custom the Authentication function
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Custom the login with either username or email
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LogoutView(View):
    """
    Log Out View
    """

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class LoginView(View):
    """
    User Login View
    """

    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        # Check if the login information meet the form requirement
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            # check whether the user login information is valid
            if user is not None:
                # check if the user is active or not
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {"msg": "用户未激活！"})

            else:
                return render(request, "login.html",
                              {"msg": "username or password is incorrect!"})
        else:
            return render(request, "login.html",
                          {"msg": "username or password is incorrect!", "login_form": login_form})


class ActiveUserView(View):
    """
    User Activation View
    """

    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        # check if the activation link is in the database
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        # if the link is not found,return activation fail page
        else:
            return render(request, "activation_fail.html")
        return render(request, "login.html")


# Register View
class RegisterView(View):
    """
    User Register View
    """

    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html",
                              {"register_form": register_form, "msg": "The account already existed in the system"})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()

            # Send the Welcome Message
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "Welcome to the Mooc Online"
            user_message.save()

            send_register_email(user_name, "register")
            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form": register_form})


class ForgetPwdView(View):
    """
    Forget Password view and Send Email Verify Email
    """

    def get(self, request):
        forget_form = ForgetPwdForm()
        return render(request, "forgetpwd.html", {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email, "forget")
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpwd.html")


class ResetView(View):
    """
    Check Reset Password Link View
    """

    def get(self, request, reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        # check if the activation link is in the database
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email": email})

        # if the link is not found,return activation fail page
        else:
            return render(request, "activation_fail.html")
        return render(request, "login.html")


# Modify Password view
class ModifyPwdView(View):
    """
    User Modify Password View
    """

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            new_password = request.POST.get("new_password", "")
            confirm_password = request.POST.get("confirm_password", "")
            email = request.POST.get("email", "")
            if new_password != confirm_password:
                render(request, "password_reset.html", {"email": email, "msg": "Two password does not match!"})
            else:
                user = UserProfile.objects.get(email=email)
                user.password = make_password(new_password)
                user.save()
                return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})


class UserInfoView(LoginRequiredMixin, View):
    """
    User Information Center Page
    """

    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    # Update the user information
    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    """
    User upload Image View
    """

    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image = image_form.cleaned_data['profile_image']
            request.user.profile_image = image
            request.user.save()
            return HttpResponse('{"status": "success"}',
                                content_type='application/json')
        else:
            return HttpResponse('{"status": "fail"}',
                                content_type='application/json')


class UpdatePwdView(View):
    """
    Update Password in the Personal Center
    """

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("new_password", "")
            pwd2 = request.POST.get("confirm_password", "")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"{error}'.format(modify_form.errors),
                                    content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    """
    Send Email Verify code for changing the registration email
    """

    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email": "The email already exists in the system"}', content_type='application/json')
        send_register_email(email, "update")
        return HttpResponse('{"status":"success","msg": "The email has been sent to your email"}',
                            content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    """
    Update Account Email View
    """

    def post(self, request):
        email = request.POST.get("email", "")
        code = request.POST.get("code", "")

        existing_record = EmailVerifyRecord.objects.filter(email=email, code=code, send_type="update")
        if existing_record:
            user = request.user
            user.email = email
            user.save()
        else:
            return HttpResponse('{"email": "Not Valid Verify Code"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    """
    My Course View
    """

    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {"user_courses": user_courses})


class MyFavOrgView(LoginRequiredMixin, View):
    """
    My Favorite Organization View
    """

    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {"org_list": org_list})


class MyFavTeacherView(LoginRequiredMixin, View):
    """
    My Favorite Teacher View
    """

    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {"teacher_list": teacher_list})


class MyFavCourseView(LoginRequiredMixin, View):
    """
    My Favorite Course View
    """

    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {"course_list": course_list})


class MyMessageView(LoginRequiredMixin, View):
    """
    My Message View
    """

    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user.id)
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        messages = Paginator(all_messages, 5, request=request)
        return render(request, "usercenter-message.html", {"messages": messages, })


class IndexView(View):
    """
    Website Index Page
    """

    def get(self, request):
        """
        Retrieve the Banner
        :param request:
        :return:  index template rendered
        """
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banners': all_banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs
        })


def page_not_found(request):
    """
    Global 404 Page
    :param request:
    :return: http response with 404 code
    """
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response

def page_error(request):
    """
    Global 500 Page
    :param request:
    :return: http response with 500 code
    """
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
