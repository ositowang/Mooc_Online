__author__ = 'osito_wang'
__date__ = '2018/6/14 13:14'

import xadmin
from xadmin import views
from xadmin.plugins.auth import UserAdmin
from xadmin.layout import Fieldset, Main, Side, Row

from .models import EmailVerifyRecord, Banner,UserProfile


# Base Settings for Xadmin

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "Mooc_Online Admin"
    site_footer = "Mooc_Online.Inc"
    menu_style = "accordion"


class UserProfileAdmin(UserAdmin):
    """
    User Admin Models
    """
    def get_form_layout(self):
        if self.org_obj:
            self.form_layout = (
                Main(
                    Fieldset('',
                             'username', 'password',
                             css_class='unsort no_title'
                             ),
                    Fieldset(_('Personal info'),
                             Row('first_name', 'last_name'),
                             'email'
                             ),
                    Fieldset(_('Permissions'),
                             'groups', 'user_permissions'
                             ),
                    Fieldset(_('Important dates'),
                             'last_login', 'date_joined'
                             ),
                ),
                Side(
                    Fieldset(_('Status'),
                             'is_active', 'is_staff', 'is_superuser',
                             ),
                )
            )
        return super(UserAdmin, self).get_form_layout()


# Applications Admin
class EmailVerifyRecordAdmin(object):
    list_display = ["code", "email", "send_type", "send_time"]
    search_fields = ["code", "email", "send_type"]
    list_filter = ["code", "email", "send_type", "send_time"]
    model_icon = 'fa fa-address-book-o'


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
