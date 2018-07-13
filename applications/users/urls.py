__author__ = 'osito_wang'
__date__ = '2018/7/6 11:46'

from django.conf.urls import url
from .views import UserInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView, MyCourseView, \
    MyFavOrgView, MyFavTeacherView, MyFavCourseView,MyMessageView

urlpatterns = [
    # user information page
    url(r'^info/$', UserInfoView.as_view(), name="user_info"),
    # User upload profile_image
    url(r'^image/upload/$', UploadImageView.as_view(), name="image_upload"),
    # Update User password in the personal center
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name="update_pwd"),
    # Send Email Verify Code for changing the registration email
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name="sendemail_code"),
    # Update Email
    url(r'^update_email/$', UpdateEmailView.as_view(), name="update_email"),
    # My Course Page
    url(r'^mycourse/$', MyCourseView.as_view(), name="my_course"),
    # My favorite Organization
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name="myfav_org"),
    # My favorite Teacher
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name="myfav_teacher"),
    # My favorite Course
    url(r'^myfav/course/$', MyFavCourseView.as_view(), name="myfav_course"),
    # My Message
    url(r'^mymessage/$', MyMessageView.as_view(), name="mymessage"),
]
