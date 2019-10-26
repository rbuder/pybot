#!/usr/bin/env python

from telegram.ext import Updater, CommandHandler
import sys
from logging import getLogger, DEBUG, WARNING, INFO, basicConfig
logger = getLogger(__name__)


from yaml import load
from argparse import ArgumentParser
from functools import wraps

from wemo import devicemanager

def logWrap(func):
    @wraps(func)
    def log(*args, **kwargs):
        logger.debug('Function called: {}'.format(func.__name__))
        return func(*args, **kwargs)
    return log

class Pybot:
    __updater = None
    __dispatcher = None
    __devices = None

    def setUpdater(self, token):
        self.__updater = Updater(token=token, use_context=True)

    def setDispatcher(self, updater):
        self.__dispatcher = self.__updater.dispatcher

    def getUpdater(self):
        return self.__updater

    def getDispatcher(self):
        return self.__dispatcher

    @logWrap
    def start(self, update, context):
        message="Hi, I'm a bot. Type /help for /help"
        self.respond(update, context, message)

    @logWrap
    def help(self, update, context):
        message="HELP:\n/start - Welcome\n/help - display this help message\n/uptime - get host uptime\n/switches - Show switches\n/toggleswitch $switch - toggle a switch\n/getswitchstate $switch"
        self.respond(update, context, message)

    @logWrap
    def uptime(self, update, context):
        import subprocess
        message = subprocess.check_output('uptime').decode()
        self.respond(update, context, message)

    @logWrap
    def getSwitchState(self, update, context):
        switchname = update.message.text.replace('/getswitchstate ','').strip()
        switchstate = devicemanager.getStateByName(switchname)
        message = '{} is {}'.format(switchname, switchstate)
        self.respond(update, context, message)

    @logWrap
    def toggleSwitch(self, update, context):
        switchname = update.message.text.replace('/toggleswitch ','').strip()
        switchstate_old = devicemanager.getStateByName(switchname)
        devicemanager.toggleDevicesByName(switchname)
        switchstate_new = devicemanager.getStateByName(switchname)
        message = 'Switched {} from {} to {}'.format(switchname, switchstate_old, switchstate_new)
        self.respond(update, context, message)

    @logWrap
    def switches(self, update, context):
        message = 'Discovered Devices: \n'
        message += '\n'.join(devicemanager.listDevicesByName())
        self.respond(update, context, message)

    # helper function to make logging ever so slightly easier
    def respond(self, update, context, message):
        logger.debug('Update: {}'.format(update))
        logger.debug('Context: {}'.format(context))
        logger.debug('Response: {}'.format(message))
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)

    @logWrap
    def run(self):
        start_handler = CommandHandler('start', self.start)
        help_handler = CommandHandler('help', self.help)
        uptime_handler = CommandHandler('uptime', self.uptime)
        getswitchstate_handler = CommandHandler('getswitchstate', self.getSwitchState)
        toggleswitch_handler = CommandHandler('toggleswitch', self.toggleSwitch)
        switches_handler = CommandHandler('switches', self.switches)
        self.__dispatcher.add_handler(start_handler)
        self.__dispatcher.add_handler(help_handler)
        self.__dispatcher.add_handler(uptime_handler)
        self.__dispatcher.add_handler(toggleswitch_handler)
        self.__dispatcher.add_handler(getswitchstate_handler)
        self.__dispatcher.add_handler(switches_handler)
        self.__updater.start_polling()

try:
    from yaml import CLoader as Loader
except:
    from yaml import Loader

parser = ArgumentParser(description="This is here mostly for Docker :)")
parser.add_argument('--token', metavar='t', type=str, help='The telegram API token')
parser.add_argument('--loglevel', metavar='l', type=str, help='Log Level [INFO, DEBUG, WARNING]')
parser.add_argument('--verbose', action='store_true', help='Log to stdout')
args = parser.parse_args()

if args.token:
    data = {'token': args.token}
else:
    with open('config.yml', 'r') as f:
        data = load(f, Loader=Loader)

if args.loglevel:
    levels = {
        'INFO': INFO,
        'DEBUG': DEBUG,
        'WARNING': WARNING
    }
    logger.setLevel(levels[args.loglevel])

if args.verbose:
    basicConfig(stream=sys.stdout)
pybot = Pybot()
pybot.setUpdater(data['token'])
pybot.setDispatcher(pybot.getUpdater())
pybot.run()