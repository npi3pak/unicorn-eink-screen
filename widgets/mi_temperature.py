import os
import logging
from datetime import datetime
import requests

class MiTemperature():
    currentTempature = ''

    def __init__(self, manager, mac, req_url):
        self.mac = mac
        self.manager = manager
        self.req_url = req_url

        # self.currentTempature = self.getValue()

    def getValue(self):
        res = requests.get(self.req_url)
        if res.ok:
            temp_k = res.json()['main']['temp']
            temp_c = str(round(temp_k - 273))
            logging.info("temp = " + temp_c)
            return temp_c

    def update(self):
        newTemp = self.getValue()
        if(self.currentTempature != newTemp):
            self.currentTempature = newTemp
            logging.info("connect")
            connected = self.manager.connect(self.mac);
            if connected:
                self.manager.sendTemperature(hex(int(self.currentTempature)).split('x')[-1]);
                self.manager.disconnect()
