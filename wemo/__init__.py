#!/usr/bin/env python

from .devicemanager import DeviceManager
from logging import getLogger
logger = getLogger(__name__)

logger.debug('Initialising device manager')
devicemanager = DeviceManager()
devicemanager.discoverWemoDevices()
logger.debug('Device manager ready')