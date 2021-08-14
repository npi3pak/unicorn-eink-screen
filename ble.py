import bluepy
import sys
import time
import struct
import argparse
import logging

class BLEManager(object):
    def __init__(self):
        super().__init__()
        self._device = None
        self._miEnabled = False
        self._customEnabled = False

    def connect(self, mac):
        conTry = 0
        maxTry = 5
        self._device = bluepy.btle.Peripheral()
        logging.info(f"Trying to connect to {mac}")
        while True:
            conTry += 1
            try:
                self._device.connect(mac)
                break
            except bluepy.btle.BTLEException as ex:
                if conTry <= maxTry:
                    logging.info(f"{ex}, retrying: {conTry}/{maxTry}")
                else:
                    logging.info(f"{ex}")
                    self.disconnect()
        logging.info(f"Connected to {mac}")

        services = self._device.getServices()
        self._services = {}
        for service in services:
            self._services[str(service.uuid)] = service
        if '00010203-0405-0607-0809-0a0b0c0d1912' in self._services:
            service = self._services['00010203-0405-0607-0809-0a0b0c0d1912']
            self._writeCharacteristic = service.getCharacteristics(forUUID='00010203-0405-0607-0809-0a0b0c0d2b12')[0]
            self._detectMi()
            return True
        else:
            logging.info("No Telink device detected.")
            self.disconnect()
            return False
        return false

    def disconnect(self):
        self._device.disconnect()

    def _detectMi(self):
        self._miEnabled = "ebe0ccb0-7a0a-4b0c-8a1a-6ff2997da3a6" in self._services
        self._customEnabled = "00001f10-0000-1000-8000-00805f9b34fb" in self._services

        if self._miEnabled:
            logging.info("Detected Mi Thermometer. Can't flash it.")
            self.disconnect()
        elif self._customEnabled:
            logging.info("Detected device with valid custom Firmware")
            service = self._services['00001f10-0000-1000-8000-00805f9b34fb']
            self._settingsCharacteristics = service.getCharacteristics(forUUID='00001f1f-0000-1000-8000-00805f9b34fb')[0]
        else:
            logging.info("Detected device with not valid Firmware. Can't flash it.")
            self.disconnect()

    def sendTemperature(self, data):
        self.sendCustomSetting('A4'+data)

    def sendCustomSetting(self, data):
        data = int(data, 16)
        # convert the integer into a bytearray
        data = data.to_bytes(data.bit_length() // 8, "big")
        try:
            self._settingsCharacteristics.write(data)
        except:
            logging.info(f"Error on sending setting 0x{data.hex()}")
            self.disconnect()
        logging.info(f"Settings 0x{data.hex()} was send successful")
