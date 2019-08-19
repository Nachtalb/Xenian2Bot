import re
from datetime import datetime, timedelta

import pytimeparse
from telegram.ext import Filters, MessageHandler

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

    def _kick(self, user: UserSettings, delta: timedelta = None):
        if check_permissions(self.chat, user.user, 'can_restrict_members'):
            return False

        if self.group_settings.dev_mode:
            return

        until = datetime.now() + (delta if delta else timedelta(minutes=1))
        self.chat.kick_member(user.user_id, until_date=until)

    @BaseCommand.command_wrapper(filters=Filters.group & OwnFilters.check_permission('can_restrict_members'))
    def kick(self):
        if not self.message.reply_to_message:
            self.message.reply_text('You have to reply to a users message.')
            return
        user = self.get_user_settings(self.message.reply_to_message.from_user)

        time_text = self.message.text.replace('/kick', '').strip()
        delta = None
        if time_text:
            delta = pytimeparse.parse(time_text)
            if delta is None:
                self.message.reply_text('Could not understand time. Use something like 10m or 1h etc.')
                return
            if not 30 < delta < 31622400:
                self.message.reply_text('Duration below 30 sec or above 366 days result in a ban. For that use /ban.')
                return
            delta = timedelta(seconds=delta)

        if self._kick(user, delta) is False:
            self.message.reply_text(f'Could not kick {user.link or user.user_fullname}')
            return
        self.chat.send_message(f'Kicked {user.link or user.user_fullname}',
                               reply_to_message_id=self.message.reply_to_message.message_id)

    @BaseCommand.command_wrapper(filters=Filters.group)
    def rules(self):
        if not self.group_settings.rules:
            return
        self.message.reply_html(self.group_settings.rules)

    @BaseCommand.command_wrapper(filters=Filters.group & OwnFilters.check_permission('can_change_info'))
    def set_rules(self):
        if not self.message.reply_to_message:
            self.message.reply_text('You have to reply to the new rules.')
            return

        self.group_settings.rules = self.message.reply_to_message.text_html
        self.group_settings.save()
        self.message.reply_text('Rules set, remove them with /clear_rules')

    @BaseCommand.command_wrapper(filters=Filters.group & OwnFilters.check_permission('can_change_info'))
    def clear_rules(self):
        self.group_settings.rules = None
        self.group_settings.save()
        self.message.reply_text('Rules cleared')

    @BaseCommand.command_wrapper(handler=MessageHandler, filters=Filters.group)
    def welcome(self):
        if not self.message.new_chat_members or not self.group_settings.welcome:
            return
        self.message.reply_text(self.group_settings.welcome)

    @BaseCommand.command_wrapper(filters=Filters.group & OwnFilters.check_permission('can_change_info'))
    def set_welcome(self):
        if not self.message.reply_to_message:
            self.message.reply_text('You have to reply to message to the new welcome message. (ATM only text)')
            return

        self.group_settings.welcome = self.message.reply_to_message.text_html
        self.group_settings.save()
        self.message.reply_text('Welcome message set, remove it with /clear_welcome')

    @BaseCommand.command_wrapper(filters=Filters.group & OwnFilters.check_permission('can_change_info'))
    def clear_welcome(self):
        self.group_settings.welcome = None
        self.group_settings.save()
        self.message.reply_text('Welcome message cleared')

    def _warn(self, user: UserSettings, count: int = None) -> bool or Warning:
        if check_permissions(self.chat, user.user, 'can_restrict_members'):
            return False

        warning = user.warnings.get_or_create(user=user, group=self.group_settings)[0]

        if count is not None:
            warning.count = count
        else:
            warning.count += 1

        if self.group_settings.dev_mode:
            return warning

        warning.save()
        return warning

    @BaseCommand.command_wrapper(filters=Filters.group & OwnFilters.check_permission('can_restrict_members'))
    def warn(self):
        if not self.message.reply_to_message:
            self.message.reply_text('You have to reply to a users message.')
            return
        user = self.get_user_settings(self.message.reply_to_message.from_user)

        count = next(iter(re.findall('(\d+)', self.message.text)), None)
        if count is not None:
            count = int(count)

        warning = self._warn(user, count)
        if warning is False:
            self.message.reply_text(f'Could not warn {user.link or user.user_fullname}')
            return

        if warning.count >= 3:
            self._ban(user)
            self.chat.send_message(f'User {user.link or user.user_fullname} was banned for reaching max warnings 3/3.',
                                   reply_to_message_id=self.message.reply_to_message.message_id)
        else:
            self.chat.send_message(f'Warned user {user.link or user.user_fullname}.'
                                   f'\n3 Warnings result in ban. User has {warning.count} warning(s).',
                                   reply_to_message_id=self.message.reply_to_message.message_id)
