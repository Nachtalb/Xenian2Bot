from datetime import datetime, timedelta

from telegram.ext import Filters

from bot.commands import BaseCommand
from bot.filters import Filters as OwnFilters
from bot.models.usersettings import UserSettings
from bot.utils.chat import check_permissions


class Group(BaseCommand):
    @BaseCommand.command_wrapper(filters=Filters.group & OwnFilters.check_permission('can_restrict_members'))
    def toggle_dev(self):
        if not check_permissions(self.chat, self.user, 'can_restrict_members'):
            return
        self.group_settings.dev_mode = not self.group_settings.dev_mode
        self.group_settings.save()
        self.message.reply_text(f'Dev mode {"on" if self.group_settings.dev_mode else "off"}')

    def _ban(self, user: UserSettings):
        if check_permissions(self.chat, user.user, 'can_restrict_members'):
            return False

        if self.group_settings.dev_mode:
            return
        self.chat.kick_member(user.user_id, until_date=1)

    @BaseCommand.command_wrapper(filters=Filters.group & OwnFilters.check_permission('can_restrict_members'))
    def ban(self):
        if not self.message.reply_to_message:
            self.message.reply_text('You have to reply to a users message.')
            return
        user = self.get_user_settings(self.message.reply_to_message.from_user)

        if self._ban(user) is False:
            self.message.reply_text(f'Could not ban {user.link or user.user_fullname}')
            return
        self.message.reply_text(f'Banned {user.link or user.user_fullname}')

    def _kick(self, user: UserSettings):
        if check_permissions(self.chat, user.user, 'can_restrict_members'):
            return False

        if self.group_settings.dev_mode:
            return

        until = datetime.now() + timedelta(minutes=1)
        self.chat.kick_member(user.user_id, until_date=until)

    @BaseCommand.command_wrapper(filters=Filters.group & OwnFilters.check_permission('can_restrict_members'))
    def kick(self):
        if not self.message.reply_to_message:
            self.message.reply_text('You have to reply to a users message.')
            return
        user = self.get_user_settings(self.message.reply_to_message.from_user)

        if self._kick(user) is False:
            self.message.reply_text(f'Could not kick {user.link or user.user_fullname}')
            return
        self.message.reply_text(f'Kicked {user.link or user.user_fullname}')

    @BaseCommand.command_wrapper(filters=Filters.group)
    def rules(self):
        self.message.reply_text('Rules')

    @BaseCommand.command_wrapper(filters=Filters.group & OwnFilters.check_permission('can_change_info'))
    def set_rules(self):
        self.message.reply_text('Set Rules')

    @BaseCommand.command_wrapper(filters=Filters.group)
    def welcome(self):
        self.message.reply_text('Welcome')

    @BaseCommand.command_wrapper(filters=Filters.group & OwnFilters.check_permission('can_change_info'))
    def set_welcome(self):
        self.message.reply_text('Set Welcome')

    @BaseCommand.command_wrapper(filters=Filters.group & OwnFilters.check_permission('can_restrict_members'))
    def warn(self):
        self.message.reply_text('Warn')
