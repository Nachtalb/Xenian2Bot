from django.contrib import admin

from bot.models.groupsettings import GroupSettings, Warnings
from bot.models.usersettings import UserSettings


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Info', {
            'fields': ('user_id', 'username', 'user_fullname')
        }),
    )

    readonly_fields = ('user_id', 'username', 'user_fullname',)
    list_display = ('user_id', 'username', 'user_fullname', 'modified', 'created')
    search_fields = ('user_id', 'username', 'user_fullname',)


@admin.register(GroupSettings)
class GroupSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Info', {
            'fields': ('group_id', 'grouptitle', 'groupname')
        }),
        ('Settings', {
            'fields': ('rules', 'welcome',),
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('dev_mode',),
        }),
    )

    list_display = ('group_id', 'grouptitle', 'groupname', 'has_rules', 'has_welcome', 'dev_mode', 'modified', 'created')
    readonly_fields = ('group_id', 'grouptitle', 'groupname')
    search_fields = ('group_id', 'grouptitle', 'groupname', 'rules', 'welcome')

    def has_rules(self, obj):
        return bool(obj.rules)

    has_rules.boolean = True

    def has_welcome(self, obj):
        return bool(obj.welcome)

    has_welcome.boolean = True


@admin.register(Warnings)
class WarningsAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'count', 'modified', 'created')
    autocomplete_fields = ('user', 'group')
