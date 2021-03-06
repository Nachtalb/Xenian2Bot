from typing import List

from telegram import Chat, Message
from telegram.ext import BaseFilter

from bot.models.usersettings import UserSettings
from bot.utils.chat import check_permissions, is_media_message


class Filters:
    class _IsMedia(BaseFilter):
        name = 'Filters.is_media'

        def filter(self, message):
            return is_media_message(message)

    is_media = _IsMedia()
    """:obj:`Filter`: Messages sent is a media file."""

    class _InChannel(BaseFilter):
        name = 'Filters.in_channel'

        def filter(self, message):
            return message.chat.type == Chat.CHANNEL

    in_channel = _InChannel()
    """:obj:`Filter`: Messages sent in a channels."""

    @staticmethod
    def text_is(texts: List[str] or str, lower: bool = False):
        """:obj:`Filter`: Messages text matches given text."""
        if isinstance(texts, str):
            texts = [texts]

        class TextIs(BaseFilter):
            name = 'Filters.text_is'

            def filter(self, message):
                if lower and message.text:
                    return message.text.lower() in texts
                return message.text in texts

        return TextIs()

    @staticmethod
    def state_is(state):
        """:obj:`Filter`: Check if the current user is in the given state."""

        class StateIs(BaseFilter):
            name = 'Filters.state_is'

            def filter(self, message):
                if not message.from_user:
                    return False
                user = UserSettings.objects.get(user_id=message.from_user.id)
                return user.state == state

        return StateIs()

    @staticmethod
    def check_permission(permission):
        """:obj:`Filter`: Check if the current user has the given permission."""

        class CheckPermission(BaseFilter):
            name = 'Filters.check_permission'

            def filter(self, message: Message) -> bool:
                return check_permissions(message.chat, message.from_user, permission)

        return CheckPermission()
