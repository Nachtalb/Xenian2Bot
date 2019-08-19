from django.db import models
from django_extensions.db.models import TimeStampedModel
from telegram import Chat, User

from bot.utils.internal import bot_not_running_protect


class GroupSettings(TimeStampedModel):
    group_id = models.fields.BigIntegerField(primary_key=True)
    _group: Chat = None  # Actual telegram User object

    grouptitle = models.fields.CharField(max_length=200, blank=True, null=True)
    groupname = models.fields.CharField(max_length=200, blank=True, null=True, default='')

    warnings = models.ManyToManyField('UserSettings', 'warned_users', symmetrical=True)

    dev_mode = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.grouptitle}@{self.groupname}'

    def save(self, **kwargs):
        if kwargs.get('auto_update', False):
            self.auto_update_values(save=False)
            kwargs.pop('auto_update')
        super().save(**kwargs)

    def auto_update_values(self, group: Chat = None, save=True) -> bool:
        group = group or self.group
        if group:
            self.grouptitle = group.title
            self.groupname = group.username or ''

            if save:
                self.save()
            return True
        return False

    @property
    @bot_not_running_protect
    def group(self) -> Chat:
        from bot.telegrambot import my_bot
        if not self._group:
            self._group = my_bot.bot.get_chat(self.group_id)
        return self._group
