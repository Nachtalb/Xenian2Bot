from django.contrib import admin

from bot.models.groupsettings import GroupSettings
from bot.models.usersettings import UserSettings


class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'username', 'user_fullname', 'modified', 'created']


admin.site.register(UserSettings, UserSettingsAdmin)


class GroupSettingsAdmin(admin.ModelAdmin):
    list_display = ['group_id', 'grouptitle', 'groupname', 'modified', 'created']


admin.site.register(GroupSettings, GroupSettingsAdmin)
