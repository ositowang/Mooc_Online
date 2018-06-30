__author__ = 'osito_wang'
__date__ = '2018/6/24 16:01'

from django.conf.urls import url, include

from .views import OrgView, AddUserQuestionView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddFavView

urlpatterns = [
    # example page for showing the inherited template
    url(r'^list/$', OrgView.as_view(), name="org_list"),
    url(r'^add_ask/$', AddUserQuestionView.as_view(), name="add_ask"),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="org_home"),
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name="org_course"),
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name="org_desc"),
    url(r'^teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name="org_teacher"),
    # Add Favorite and Cancel Favorite
    url(r'^add_fav/$', AddFavView.as_view(), name="add_fav"),

]
