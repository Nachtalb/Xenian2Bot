from django.template.loader import get_template
from telegram import ParseMode, ReplyKeyboardMarkup
from telegram.ext import CallbackQueryHandler, MessageHandler
from telegram.ext.filters import Filters

from bot.commands import BaseCommand
from bot.filters import Filters as OwnFilters
from bot.models.usersettings import UserSettings
from bot.utils.chat import build_menu


class Builtins(BaseCommand):

    @BaseCommand.command_wrapper(filters=Filters.private)
    def help(self):
        self.message.reply_html(get_template('commands/builtins/help.html').render())

    @BaseCommand.command_wrapper(CallbackQueryHandler, pattern='^(home|cancel)$')
    @BaseCommand.command_wrapper(MessageHandler,
                                 filters=Filters.private & OwnFilters.text_is(['cancel', 'home', 'reset'], lower=True))
    @BaseCommand.command_wrapper(names=['start', 'reset', 'cancel'], filters=Filters.private)
    def start(self):
        if self.update.callback_query:
            self.update.callback_query.answer()
            self.message.delete()

        elif 'start' in self.message.text:
            self.message.reply_html(get_template('commands/builtins/start.html').render())

        if self.message.text.lower() in ['cancel', 'home', 'reset'] and self.user_settings.state != UserSettings.IDLE:
            self.message.reply_text('Current action was cancelled')

        self.user_settings.current_channel = None
        self.user_settings.state = UserSettings.IDLE
        header, middle, footer = BaseCommand._start_buttons

        buttons = build_menu(*middle, header_buttons=header, footer_buttons=footer)
        self.message.reply_text('What do you want to do?', reply_markup=ReplyKeyboardMarkup(buttons))

    BaseCommand.register_home(start)

    @BaseCommand.command_wrapper()
    def id(self):
        message = self.message.reply_to_message or self.message
        forwarded = bool(message.forward_from_message_id)
        message_id = message.forward_from_message_id if forwarded else message.message_id
        chat_id = getattr(message.forward_from_chat if forwarded else message.chat, 'id', None)
        user_id = getattr(message.forward_from if forwarded else message.from_user, 'id', None)
        self.message.reply_text(f'UserID `{user_id}`, ChatID `{chat_id}`, MessageID `{message_id}`',
                                parse_mode=ParseMode.MARKDOWN)
