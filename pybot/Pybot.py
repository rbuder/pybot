#!/usr/bin/env python

from telegram.ext import Updater, CommandHandler

from logging import getLogger
logger = getLogger(__name__)

class Pybot:
    def start(self, update, context):
        context.bot.send_message(chat_od=update.effective_chat.id, text="Type /help for help")

    def help(self, update, context):
        context.bot.send_message(chat_od=update.effective_chat.id, text="Nothing here yet, just testing line breaks</ br>This was a HTML line break\nThis was a Unix one")
    
    def run(self):
        dispatcher = updater.dispatcher
        start_handler = CommandHandler('start', self.start)
        help_handler = CommandHandler('help', self.help)
        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(help_handler)
        updater.start_polling()