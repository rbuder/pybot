#!/usr/bin/env python

import pywemo, logging
from common import logWrap

logger = logging.getLogger(__name__)

class DeviceManager:
    __devices = None
    __state = {
        0 : 'OFF',
        1 : 'ON'
    }

    @logWrap
    def discoverWemoDevices(self):
        try:
            self.__devices = pywemo.discover_devices()
            return None
        except Exception as e:
            return e

    @logWrap
    def listDevicesByName(self):
        try:
            devices = [device.name for device in self.__devices]
            return devices
        except TypeError as e:
            return []

    @logWrap
    def getDeviceByName(self, name):
        return [device for device in self.__devices if device.name == name][0]

    @logWrap
    def toggleDevicesByName(self, name):
        device = self.getDeviceByName(name)
        try:
            return device.toggle()
        except Exception as e:
            return e

    @logWrap
    def powerOffByName(self, name):
        dev = self.getDeviceByName(name)
        try:
            return dev.off()
        except Exception as e:
            return e

    @logWrap
    def powerOnByName(self, name):
        dev = self.getDeviceByName(name)
        try:
            return dev.on()
        except Exception as e:
            return e

    @logWrap
    def getStateByName(self, name):
        dev = self.getDeviceByName(name)
        try:
            # Force update on get_State, since externally switched devices may not report the correct state
            return self.__state[dev.get_state(force_update=True)]
        except Exception as e:
            return e