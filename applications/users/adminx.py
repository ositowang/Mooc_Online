__author__ = 'osito_wang'
__date__ = '2018/6/14 13:14'

import xadmin
from xadmin import views
from .models import EmailVerifyRecord, Banner


# Base Settings for Xadmin

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "Mooc_OnlineAdmin"
    site_footer = "Mooc_Online.Inc"
    menu_style = "accordion"


# Applications Admin
class EmailVerifyRecordAdmin(object):
    list_display = ["code", "email", "send_type", "send_time"]
    search_fields = ["code", "email", "send_type"]
    list_filter = ["code", "email", "send_type", "send_time"]


class BannerAdmin(object):
    list_display = ["title", "image", "url", "index", "add_time"]
    search_fields = ["code", "email", "send_type", "index"]
    list_filter = ["title", "image", "url", "index", "add_time"]


# Register the applications
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)

# Register the xadmin settings for the website
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
