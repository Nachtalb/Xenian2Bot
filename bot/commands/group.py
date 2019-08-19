from telegram.ext import Filters

from bot.commands import BaseCommand
from bot.models.usersettings import UserSettings


class Group(BaseCommand):
    @BaseCommand.command_wrapper(filters=Filters.group)
    def toggle_dev(self):
        self.group_settings.dev_mode = not self.group_settings.dev_mode
        self.group_settings.save()
        self.message.reply_text(f'Dev mode {"on" if self.group_settings.dev_mode else "off"}')

    @BaseCommand.command_wrapper(filters=Filters.group)
    def ban(self):
        self.message.reply_text('Ban')

    def _kick(self, user: UserSettings):
        if not self.group_settings.dev_mode:
            self.chat.kick_member(user.user_id)

    @BaseCommand.command_wrapper(filters=Filters.group)
    def kick(self):
        if not self.message.reply_to_message:
            self.message.reply_text('You have to reply to a users message.')
            return
        user = self.get_user_settings(self.message.reply_to_message.from_user)

        self._kick(user)

        self.message.reply_text(f'Kicked {user.link or user.user_fullname}')

    @BaseCommand.command_wrapper(filters=Filters.group)
    def rules(self):
        self.message.reply_text('Rules')

    @BaseCommand.command_wrapper(filters=Filters.group)
    def set_rules(self):
        self.message.reply_text('Set Rules')

    @BaseCommand.command_wrapper(filters=Filters.group)
    def welcome(self):
        self.message.reply_text('Welcome')

    @BaseCommand.command_wrapper(filters=Filters.group)
    def set_welcome(self):
        self.message.reply_text('Set Welcome')

    @BaseCommand.command_wrapper(filters=Filters.group)
    def warn(self):
        self.message.reply_text('Warn')
