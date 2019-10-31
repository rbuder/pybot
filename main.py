#!/usr/bin/env python

# from telegram.ext import Updater, CommandHandler

from mmpy_bot import settings, bot
from mmpy_bot.bot import respond_to
import sys, random, string
from logging import getLogger, DEBUG, WARNING, INFO, basicConfig
logger = getLogger(__name__)

from yaml import load
from argparse import ArgumentParser

from common import logWrap

from wemo import devicemanager

@logWrap
@respond_to('start')
def start(message):
    response="Hi, I'm a bot."
    logger.debug('Message: {}'.format(message))
    logger.debug('Response: {}'.format(response))
    message.reply(response)

@logWrap
@respond_to('uptime')
def uptime(message):
    import subprocess
    response = subprocess.check_output('uptime').decode()
    message.reply(response)

@logWrap
@respond_to('rescan')
def rescan(message):
    devicemanager.discoverWemoDevices()
    response = '\n'.join(devicemanager.listDevicesByName())
    message.reply(response)

@logWrap
@respond_to('switchstate (.*)')
def getSwitchState(message, switch):
    switchname = switch.strip()
    switchstate = devicemanager.getStateByName(switchname)
    response = '{} is {}'.format(switchname, switchstate)
    message.reply(response)

@logWrap
@respond_to('toggleswitch (.*)')
def toggleSwitch(message, switch):
    switchname = switch.strip()
    switchstate_old = devicemanager.getStateByName(switchname)
    devicemanager.toggleDevicesByName(switchname)
    switchstate_new = devicemanager.getStateByName(switchname)
    response = 'Switched {} from {} to {}'.format(switchname, switchstate_old, switchstate_new)
    message.reply(response)

@logWrap
@respond_to('switches')
def switches(message):
    response = 'Discovered Devices: \n'
    response += '\n'.join(devicemanager.listDevicesByName())
    message.reply(response)

try:
    from yaml import CLoader as Loader
except:
    from yaml import Loader

parser = ArgumentParser(description="This is here mostly for Docker :)")
parser.add_argument('--loglevel', metavar='l', type=str, help='Log Level [INFO, DEBUG, WARNING]')
parser.add_argument('--verbose', action='store_true', help='Log to stdout')
args = parser.parse_args()

with open('./config/config.yml', 'r') as f:
    data = load(f, Loader=Loader)

if args.loglevel:
    levels = {
        'INFO': INFO,
        'DEBUG': DEBUG,
        'WARNING': WARNING
    }
    logger.setLevel(levels[args.loglevel])

logger.debug('Config loaded')

mmpy_bot_settings = data.get('mmpy_bot')
for k in mmpy_bot_settings.keys():
    setattr(settings, k, mmpy_bot_settings.get(k))
    logger.debug('Setting {} to {}'.format(k, getattr(settings, k)))

logger.debug('Initialising bot...')

bot.settings = settings
pybot = bot.Bot()
pybot.run()

logger.info('Bot running... happy chatting!')