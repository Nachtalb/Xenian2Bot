from cached_property import cached_property_ttl
from django.db import models
from django_extensions.db.models import TimeStampedModel
from telegram import User

from bot.utils.internal import bot_not_running_protect


class UserSettings(TimeStampedModel):
    IDLE = 'idle'

    STATES = (IDLE)

    user_id = models.fields.BigIntegerField(primary_key=True)
    _user: User = None  # Actual telegram User object
    _user_state = models.fields.CharField(max_length=100,
                                          choices=map(lambda s: (s, s), STATES),
                                          default=IDLE,
                                          verbose_name='State')

    username = models.fields.CharField(max_length=200, blank=True, null=True)
    user_fullname = models.fields.CharField(max_length=200)

    def __str__(self):
        return f'{self.user_id}@{self.username}'

    def save(self, **kwargs):
        if kwargs.get('auto_update', False):
            self.auto_update_values(save=False)
            kwargs.pop('auto_update')
        super().save(**kwargs)

    @property
    def state(self):
        return self._user_state

    @state.setter
    def state(self, value):
        if value not in self.STATES:
            raise KeyError('State does no exists')

        self._user_state = value
        self.save()

    def auto_update_values(self, user: User = None, save=True) -> bool:
        user = user or self.user
        if user:
            self.username = user.username
            self.user_fullname = user.full_name

            if save:
                self.save()
            return True
        return False

    @cached_property_ttl(ttl=3600)
    @bot_not_running_protect
    def link(self) -> str:
        return self.user.link

    @property
    @bot_not_running_protect
    def user(self) -> User:
        from bot.telegrambot import my_bot
        if not self._user:
            self._user = my_bot.bot.get_chat(self.user_id)
        return self._user
