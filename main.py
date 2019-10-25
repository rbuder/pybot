#!/usr/bin/env python

from telegram.ext import Updater, CommandHandler

from logging import getLogger
logger = getLogger(__name__)

class Pybot:
    __updater = None
    __dispatcher = None

    def setUpdater(self, token):
        self.__updater = Updater(token=token, use_context=True)

    def setDispatcher(self, updater):
        self.__dispatcher = self.__updater.dispatcher

    def getUpdater(self):
        return self.__updater

    def getDispatcher(self):
        return self.__dispatcher

    def start(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Type /help for help")

    def help(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="HELP:\n/start - Welcome\n/help - display this help message\n/uptime - get host uptime")

    def uptime(self, update, context):
        import subprocess
        context.bot.send_message(chat_id=update.effective_chat.id, text=subprocess.check_output('uptime').decode())

    def run(self):
        start_handler = CommandHandler('start', self.start)
        help_handler = CommandHandler('help', self.help)
        uptime_handler = CommandHandler('uptime', self.uptime)
        self.__dispatcher.add_handler(start_handler)
        self.__dispatcher.add_handler(help_handler)
        self.__dispatcher.add_handler(uptime_handler)
        self.__updater.start_polling()

pybot = Pybot()
pybot.setUpdater('TOKEN')
pybot.setDispatcher(pybot.getUpdater())
pybot.run()