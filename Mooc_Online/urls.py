"""Mooc_Online URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.static import serve

import xadmin
from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView, LogoutView, \
    IndexView
from Mooc_Online.settings import MEDIA_ROOT

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    # Website Index Page Url
    url('^$', IndexView.as_view(), name="index"),
    # Log In Url
    url('^login/$', LoginView.as_view(), name="login"),
    # Log Out Url
    url('^logout/$', LogoutView.as_view(), name="logout"),
    # User Registration Url
    url('^register/$', RegisterView.as_view(), name="register"),
    # Captcha Url
    url(r'^captcha/', include('captcha.urls')),
    # User Activiation Url
    url(r'^activate/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_activation"),
    url(r'^forget/$', ForgetPwdView.as_view(), name="forget_password"),
    url(r'^reset/(?P<reset_code>.*)/$', ResetView.as_view(), name="reset_password"),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name="modify_password"),

    # Organization Url Configuration
    url(r'^org/', include('organization.urls', namespace="organization")),

    # Course Url Configuration
    url(r'^course/', include('course.urls', namespace="course")),

    # User Url Configuration
    url(r'^users/', include('users.urls', namespace="users")),

    # Configure the uploaded files path url
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    # url(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),

    # Ueditor Url
    url(r'^ueditor/', include('DjangoUeditor.urls')),

]
# Global 404
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'
