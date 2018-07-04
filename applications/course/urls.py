__author__ = 'osito_wang'
__date__ = '2018/6/30 11:16'

from django.conf.urls import url
from course.views import CourseListView, CourseDetailView, CourseInfoView, CommentsView, AddCommentView, VideoPlayView

urlpatterns = [
    # Course List Url
    url(r'^list/$', CourseListView.as_view(), name="course_list"),
    # Course Detail Url
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),
    # Course Chapter Url
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name="course_info"),
    # Course Comment Url
    url(r'^comment/(?P<course_id>\d+)/$', CommentsView.as_view(), name="course_comment"),
    # Add Comment Url
    url(r'^add_comment/$', AddCommentView.as_view(), name="add_comment"),
    # Chapter Video Url
    url(r'^video/(?P<video_id>\d+)/$', VideoPlayView.as_view(), name="video_play"),

]
