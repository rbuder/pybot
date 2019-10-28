#!/usr/bin/env python

import pywemo

class DeviceManager:
    __devices = None
    __state = {
        0 : 'OFF',
        1 : 'ON'
    }

    def discoverWemoDevices(self):
        try:
            self.__devices = pywemo.discover_devices()
            return None
        except Exception as e:
            return e

    def listDevicesByName(self):
        return [device.name for device in self.__devices]

    def getDeviceByName(self, name):
        return [device for device in self.__devices if device.name == name][0]

    def toggleDevicesByName(self, name):
        device = self.getDeviceByName(name)
        try:
            return device.toggle()
        except Exception as e:
            return e

    def powerOffByName(self, name):
        dev = self.getDeviceByName(name)
        try:
            return dev.off()
        except Exception as e:
            return e

    def powerOnByName(self, name):
        dev = self.getDeviceByName(name)
        try:
            return dev.on()
        except Exception as e:
            return e

    def getStateByName(self, name):
        dev = self.getDeviceByName(name)
        try:
            # Force update on get_State, since externally switched devices may not report the correct state
            return self.__state[dev.get_state(force_update=True)]
        except Exception as e:
            return e
