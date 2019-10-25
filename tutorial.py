#!/usr/bin/env python

from telegram.ext import Updater
updater = Updater(token='910333639:AAFT6tirAyhD1-Dcb9KWaXQbKezbL57MtPU', use_context=True)

dispatcher = updater.dispatcher

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

import subprocess

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me")

def uptime(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=subprocess.check_output('uptime').decode())

from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
uptime_handler = CommandHandler('uptime', uptime)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(uptime_handler)

updater.start_polling()